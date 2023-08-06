#!/usr/bin/python
# -*- coding: utf-8 -*-

# bittrex_websocket/websocket_client.py
# Stanislav Lazarov

####
# NEW
import asyncio
import uvloop
import sys

# sys.path.insert(0, '/Users/slazarov/Documents/Python-Projects/python-signalr-client')
# from signalr_aio import Connection
from ._signalr import Connection
####

# from ._signalr import Connection
import logging
from abc import ABCMeta, abstractmethod
from threading import Thread, current_thread
from time import sleep, time
# from ._exceptions import *

from ._auxiliary import BittrexConnection, process_message, update_invokes
from ._logger import add_stream_logger, remove_stream_logger
from ._queue_events import *
from .constants import *
from collections import deque

logger = logging.getLogger(__name__)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class WebSocket(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def subscribe_to_orderbook(self, tickers):
        """
        Subscribe and maintain the live order book for a set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        raise NotImplementedError("Should implement subscribe_to_orderbook()")

    @abstractmethod
    def subscribe_to_orderbook_update(self, tickers):
        """
        Subscribe to order book updates for a set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        raise NotImplementedError("Should implement subscribe_to_orderbook_update")

    @abstractmethod
    def subscribe_to_trades(self, tickers):
        """
        Subscribe and receive tick data(executed trades) for a set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        raise NotImplementedError("Should implement subscribe_to_trades()")

    @abstractmethod
    def subscribe_to_ticker_update(self, tickers=None):
        """
        Subscribe and receive general data updates for a set of ticker(s). Example output:

        {
            'MarketName': 'BTC-ADA',
            'High': 7.65e-06,
            'Low': 4.78e-06,
            'Volume': 1352355429.5288217,
            'Last': 7.2e-06,
            'BaseVolume': 7937.59243908,
            'TimeStamp': '2017-11-28T15:02:17.7',
            'Bid': 7.2e-06,
            'Ask': 7.21e-06,
            'OpenBuyOrders': 4452,
            'OpenSellOrders': 3275,
            'PrevDay': 5.02e-06,
            'Created': '2017-09-29T07:01:58.873'
        }

        :param tickers: A list of tickers you are interested in.
        :type tickers: [] or None
        """
        raise NotImplementedError("Should implement subscribe_to_ticker_update()")

    @abstractmethod
    def unsubscribe_from_orderbook(self, tickers):
        """
        Unsubscribe from real time order for specific set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        raise NotImplementedError("Should implement unsubscribe_to_orderbook()")

    @abstractmethod
    def unsubscribe_from_orderbook_update(self, tickers):
        """
        Unsubscribe from order book updates for a set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        raise NotImplementedError("Should implement unsubscribe_to_orderbook_update")

    @abstractmethod
    def unsubscribe_from_trades(self, tickers):
        """
        Unsubscribe from receiving tick data(executed trades) for a set of ticker(s)

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        raise NotImplementedError("Should implement unsubscribe_to_trades()")

    @abstractmethod
    def unsubscribe_from_ticker_update(self, tickers=None):
        """
        Unsubscribe from receiving general data updates for a set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: [] or None
        """
        raise NotImplementedError("Should implement unsubscribe_to_ticker_update()")

    @abstractmethod
    def get_order_book(self, ticker=None):
        """
        Returns the most recently updated order book for the specific ticker.
        If no ticker is specified, returns a dictionary with the order books of
        all subscribed tickers.

        :param ticker: The specific ticker you want the order book for.
        :type ticker: str
        """
        raise NotImplementedError("Should implement get_order_book()")

    @abstractmethod
    def get_order_book_sync_state(self, tickers=None):
        """
        Returns the sync state of the order book for the specific ticker(s).
        If no ticker is specified, returns the state for all tickers.
        The sync states are:

            Not initiated = 0
            Invoked, not synced = 1
            Received, not synced, not processing = 2
            Received, synced, processing = 3

        :param tickers: The specific ticker(s) and it's order book sync state you are interested in.
        :type tickers: []
        """
        raise NotImplementedError("Should implement get_order_book_sync_state()")

    @abstractmethod
    def disconnect(self):
        """
        Disconnects the connections and stops the websocket instance.
        """
        raise NotImplementedError("Should implement disconnect()")

    @staticmethod
    @abstractmethod
    def enable_log(file_name=None):
        """
        Enables logging.

        :param file_name: The name of the log file, located in the same directory as the executing script.
        :type file_name: str
        """
        raise NotImplementedError("Should implement enable_log()")

    @staticmethod
    @abstractmethod
    def disable_log():
        """
        Disables logging.
        """
        raise NotImplementedError("Should implement disable_log()")


class BittrexSocket(WebSocket):
    def __init__(self):
        self.socket_loop = None
        self.control_queue = None
        self.threads = {}
        self.tasks = {}
        self.connections = {}
        self.invokes = []
        self.order_books = {}
        self.tickers = Ticker()
        self.max_tickers_per_conn = 30
        self._start_main_thread()

    # ===========================
    # Main Thread Private Methods
    # ===========================

    def _start_main_thread(self):

        def start():
            asyncio.ensure_future(self.control_queue_handler(), loop=self.socket_loop)
            self.socket_loop.run_forever()

        self.on_open()
        self.socket_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.socket_loop)
        self.control_queue = asyncio.Queue(loop=self.socket_loop)

        thread = Thread(target=start, daemon=True, name='BittrexSocketControlQueue')
        self.threads[thread.getName()] = thread
        thread.start()

    async def control_queue_handler(self):
        while True:
            control_event = await self.control_queue.get()
            if control_event is not None:
                if control_event.type == 'CONNECT':
                    await self._handle_connect(control_event)
                elif control_event.type == 'SUBSCRIBE':
                    await self._handle_subscribe(control_event)
                elif control_event.type == 'IS_FIRST_RUN':
                    await self._handle_is_first_run(control_event)
                elif control_event.type == 'ORDER':
                    await self._handle_order(control_event)
                elif control_event.type == 'SNAPSHOT':
                    await self._handle_snapshot(control_event)
                # if event.type == 'INVOKE':
                #     await ws.send(dumps(event.message))
                # elif event.type == 'CLOSE':
                #     await ws.close(code=1000, reason='lol')
                self.control_queue.task_done()

    @staticmethod
    async def connection_handler(conn_event):
        try:
            conn_event.conn_obj.conn.start()
            logger.info('Establishing connection to Bittrex.')
        except Exception as e:
            print(e)

    # ---------------------
    # Control Queue Methods
    # ---------------------

    def _start_socket_control_queue(self):
        """
        Handles the communication with Bittrex, namely
        starting/closing a connection and un/subscribing to channels
        It stays idle until a command is send to it.
        """
        while True:
            try:
                control_event = self.control_queue.get()
            except queue.Empty:
                pass
            else:
                if control_event is not None:
                    if control_event.type == 'CONNECT':
                        self._handle_connect(control_event)
                    elif control_event.type == 'DISCONNECT':
                        if self._handle_disconnect(control_event):
                            self.on_close()
                            break
                    elif control_event.type == 'SUBSCRIBE':
                        self._handle_subscribe(control_event)
                    elif control_event.type == 'SUBSCRIBE_INTERNAL':
                        self._handle_subscribe_internal(control_event)
                    elif control_event.type == 'UNSUBSCRIBE':
                        self._handle_unsubscribe(control_event)
                    elif control_event.type == 'SNAPSHOT':
                        self._handle_get_snapshot(control_event)
                    elif control_event.type == 'IS_FIRST_RUN':
                        self._handle_is_first_run(control_event)
                    elif control_event.type == 'IS_RUNNING':
                        self._handle_is_running(control_event)
                    elif control_event.type == 'RECONNECT':
                        self._handle_reconnect(control_event)
                    self.control_queue.task_done()

    async def _handle_connect(self, conn_event):
        """
        Prepares and starts new thread for a new Bittrex connection.

        :param conn_event: Contains the connection object.
        :type conn_event: ConnectEvent
        """
        self.connections.update({conn_event.conn_obj.id: conn_event.conn_obj})
        asyncio.ensure_future(self.connection_handler(conn_event), loop=self.socket_loop)

    def _init_connection(self, conn_obj):
        """
        Initiates the Bittrex connection and assigns event handlers.

        :param conn_obj: The Bittrex connection object
        :type conn_obj: BittrexConnection
        """

        def reload_generator():
            gen = (url for url in urls)
            return gen

        def get_url(url_list):
            result = next(url_list)
            return result

        def is_next_url():
            # (1) Reloads the url generator if n seconds have passed
            # (2) Refreshes the session cookie.
            # ---------------------------------------------------------------------------
            # Nonlocal statement is not available in Python 2.X
            # So we are using a workaround that imitates 'self' for nested functions.
            # In this way we can edit variables that are external to the nested function.
            # ---------------------------------------------------------------------------
            if runtime is not None and time() - runtime > 600:
                self_workaround['urls'] = reload_generator()
            self_workaround['connection'] = self._create_cookie()
            return self_workaround

        urls = ['https://socket-beta.bittrex.com/signalr',
                'https://socket-stage.bittrex.com/signalr',
                'https://socket.bittrex.com/signalr']
        conn, corehub, conn_id = conn_obj.conn, conn_obj.corehub, conn_obj.id
        self_workaround = {'urls': reload_generator(), 'connection': conn}
        runtime = None
        while True:
            try:
                try:
                    # Get the variables from the dict into separate variables.
                    # Check is_next_url() for explanation
                    url_gen = self_workaround['urls']
                    conn = self_workaround['connection']
                    # Actual part
                    conn.url = get_url(url_gen)
                    logger.info(MSG_INFO_CONN_ESTABLISHING.format(conn_id, conn.url))
                    conn.start()
                    runtime = time()
                    conn_obj.activate()
                    logger.info(MSG_INFO_CONNECTED.format(conn_id, conn.url))
                    # Add handlers
                    corehub.client.on('updateExchangeState', self._on_tick_update)
                    corehub.client.on('updateSummaryState', self._on_ticker_update)
                    run = conn.wait(5400)
                    # When we purposely close the connection, the script will exit conn.wait()
                    # so we need to inform the script that it should not try to reconnect.
                    if conn_obj.close_me is True:
                        return
                    elif run is not None:
                        logger.error(MSG_ERROR_GEVENT.format(conn_id, type(run)))
                        self._empty_conn_id(conn_id)
                        return
                    is_next_url()
                except HTTPError:
                    # Related to wrong url. Will be raised in case Bittrex changes it's url or you touched it!
                    logger.error(MSG_ERROR_CONN_HTTP.format(conn_id, conn.url))
                    is_next_url()
                except MissingSchema:
                    logger.error(MSG_ERROR_CONN_MISSING_SCHEMA.format(conn_id, conn.url))
                    is_next_url()
                except WebSocketConnectionClosedException:
                    logger.error(WebSocketConnectionClosedException)
                    is_next_url()
                    raise ImportWarning(MSG_ERROR_SOCKET_WEBSOCKETCONNECTIONCLOSED)
                except WebSocketBadStatusException:
                    # This should be related to Cloudflare.
                    logger.error(WebSocketBadStatusException)
                    is_next_url()
                    raise ImportWarning(MSG_ERROR_SOCKET_WEBSOCKETBADSTATUS)
                except SocketError:
                    logger.error(MSG_ERROR_CONN_SOCKET.format(conn_id, conn.url))
                    is_next_url()
            except StopIteration:
                logger.error(MSG_ERROR_CONN_FAILURE.format(conn_id))
                self._empty_conn_id(conn_id)
                return

    def _empty_conn_id(self, conn_id):
        self.connections.pop(conn_id)
        subs = self.tickers.sort_by_conn_id(conn_id)
        for sub_type in subs.keys():
            for ticker in subs[sub_type]:
                if self.tickers.get_sub_state(ticker, sub_type) is SUB_STATE_ON:
                    self.tickers.change_sub_state(ticker, sub_type, SUB_STATE_OFF)
        for sub_type in subs.keys():
            for ticker in subs[sub_type]:
                # if self.tickers.get_sub_state(ticker, sub_type) is SUB_STATE_ON:
                params = [[ticker], sub_type, None]
                if sub_type is SUB_TYPE_ORDERBOOK:
                    params[2] = self.tickers.get_book_depth(ticker)
                event = ReconnectEvent(*params)
                self.control_queue.put(event)
                while self.tickers.get_sub_state(ticker, sub_type) is True:
                    sleep(1)
                while self.tickers.get_sub_state(ticker, sub_type) is False:
                    sleep(1)

    def _handle_disconnect(self, disconn_event):
        """
        Handles the event of disconnecting connections.

        :type disconn_event: The disconnect event.
        :type disconn_event: DisconnectEvent
        :return: True = all connections have to be closed; False = specific connection has to be closed.
        :rtype: bool
        """

        # Find whether we are closing all connections or just one.
        if disconn_event.conn_object is None:
            conns = self.connections.values()
            msg = 'Sending a close signal to all connections.'
            flag = True
        else:
            conns = disconn_event.conn_object
            msg = 'Sending a close signal to connection {}'.format(conns[0].id)
            flag = False

        # Closing a connection from an external error results in an error.
        # We set a close_me flag so that next time when a message is received
        # from the thread that started the connection, a method will be called to close it.
        for conn in conns:
            logger.info(msg)
            conn.close()
            while conn.state:
                sleep(0.5)
            logger.info('Connection {} has been successfully closed.'.format(conn.id))
        return flag

    async def _handle_subscribe(self, sub_event):
        """
        Handles the event of subscribing a specific ticker to a specific subscription type.

        :param sub_event: The ticker subscription event
        :type sub_event: SubscribeEvent
        :return: False = Subscribing failed because the connection is not active.
        :rtype: bool
        """
        conn = sub_event.conn_object
        tickers = sub_event.tickers
        sub_type = sub_event.sub_type
        invoke = sub_event.invoke
        for ticker in tickers:
            update_invokes(self.invokes, conn, invoke, ticker)
            conn.corehub.server.invoke(invoke, ticker)
        self.tickers.enable(tickers, sub_type, conn.id)

    def _handle_subscribe_internal(self, sub_event):
        """
        If the ticker is already in the tickers list and it shares a subscription
        callback for the new subscription request, then we don't have to invoke
        a request to Bittrex but only enable the subscription state internally,
        because the messages are received but are filtered.

        :param sub_event: The internal subscribe event.
        :type sub_event: SubscribeInternalEvent
        """
        tickers = sub_event.tickers
        conn = sub_event.conn_object
        sub_type = sub_event.sub_type
        self.tickers.enable(tickers, sub_type, conn.id)

    def _handle_unsubscribe(self, unsub_event):
        """
        Handles the event of revoking a specific active subscription
        for a specific ticker. Also if no active subscriptions remain,
        the websocket client is closed.

        :param unsub_event: The ticker unsubscribe event.
        :type unsub_event: UnsubscribeEvent
        """
        ticker, sub_type, conn_id = unsub_event.ticker, unsub_event.sub_type, unsub_event.conn_id
        self.tickers.disable(ticker, sub_type)
        # Wait for the subscription to deactivate
        # In the case of sync loss, the subscription will be deactivated earlier from _sync_order_book
        while self.tickers.get_sub_state(ticker, sub_type) is SUB_STATE_ON:
            sleep(0.5)
        if unsub_event.unsub_type is True:
            self._is_no_subs_active()
        # self.tickers.remove(ticker)

    def _handle_get_snapshot(self, snapshot_event):
        """
        Requests an order book snapshot request from Bittrex.

        :param snapshot_event: The ticker snapshot event.
        :type snapshot_event: SnapshotEvent
        """
        conn, ticker = snapshot_event.conn_object, snapshot_event.ticker
        method = 'queryExchangeState'
        try:
            logger.info(MSG_INFO_ORDER_BOOK_REQUESTED.format(SUB_TYPE_ORDERBOOK, ticker))
            conn.corehub.server.invoke(method, ticker)
            self.tickers.set_snapshot_state(ticker, SNAPSHOT_SENT)
        except Exception as e:
            print(e)
            print('Failed to invoke snapshot query')

    def _handle_reconnect(self, reconnect_event):
        ticker, sub_type, book_depth = reconnect_event.tickers, reconnect_event.sub_type, reconnect_event.book_depth

        logger.info(MSG_INFO_RECONNECT.format(sub_type, ticker))

        if sub_type == SUB_TYPE_ORDERBOOK:
            self.unsubscribe_from_orderbook(ticker, False)
        elif sub_type == SUB_TYPE_ORDERBOOKUPDATE:
            self.unsubscribe_from_orderbook_update(ticker, False)
        elif sub_type == SUB_TYPE_TRADES:
            self.unsubscribe_from_trades(ticker, False)
        elif sub_type == SUB_TYPE_TICKERUPDATE:
            self.unsubscribe_from_ticker_update(ticker, False)

        if sub_type == SUB_TYPE_ORDERBOOK:
            self.subscribe_to_orderbook(ticker, book_depth)
        elif sub_type == SUB_TYPE_ORDERBOOKUPDATE:
            self.subscribe_to_orderbook_update(ticker)
        elif sub_type == SUB_TYPE_TRADES:
            self.subscribe_to_trades(ticker)
        elif sub_type == SUB_TYPE_TICKERUPDATE:
            self.subscribe_to_ticker_update(ticker)

    def _is_first_run(self, tickers, sub_type):
        # Check if the websocket has been initiated already or if it's the first run.
        if not self.tickers.list:
            self._subscribe_first_run(tickers, sub_type)
        else:
            return False

    def _subscribe_first_run(self, tickers, sub_type, objects=None):
        if objects is None:
            objects = self._create_bittrex_connection(tickers)
        for obj in objects:
            connect_event = ConnectEvent(obj[1])
            asyncio.Task(self.control_queue.put(connect_event), loop=self.socket_loop)
            subscribe_event = SubscribeEvent(obj[0], obj[1], sub_type)
            asyncio.Task(self.control_queue.put(subscribe_event), loop=self.socket_loop)

    def _unsubscribe(self, tickers, sub_type, unsub_type):
        for ticker in tickers:
            event = UnsubscribeEvent(ticker, self.tickers, sub_type, unsub_type)
            self.control_queue.put(event)

    async def _handle_is_first_run(self, is_first_run_event):
        tickers, sub_type = is_first_run_event.tickers, is_first_run_event.sub_type
        sub_states = self.tickers.sort_by_sub_state()
        if not sub_states:
            # No initiated connections yet.
            self._subscribe_first_run(tickers, sub_type)
        # elif len(sub_states) == 1 and False in sub_states:
        #     self._subscribe_first_run(tickers, sub_type)
        # elif not self.connections:
        #     self._subscribe_first_run(tickers, sub_type)
        # else:
        #     self.control_queue.put(IsRunningEvent(tickers, sub_type))
        #     # self._is_running(tickers, sub_type)

    def _handle_is_running(self, is_running_event):
        tickers, sub_type = is_running_event.tickers, is_running_event.sub_type
        # Check for existing connections
        # if self.connections:
        events = []
        # Check for already existing tickers and enable the subscription before opening a new connection.
        for ticker in tickers:
            if self.tickers.get_sub_state(ticker, sub_type) is SUB_STATE_ON:
                logger.info('{} subscription is already enabled for {}. Ignoring...'.format(sub_type, ticker))
            else:
                # Assign most suitable connection
                event = self._assign_conn(ticker, sub_type)
                events.append(event)
        for event in events:
            self.control_queue.put(event[0])

    def _get_snapshot(self, tickers):
        for ticker_name in tickers:
            # ticker_object = self.tickers.list[ticker_name]
            conn_id = self.tickers.get_sub_type_conn_id(ticker_name, SUB_TYPE_ORDERBOOK)
            # Due to multithreading the connection might not be added to the connection list yet
            while True:
                try:
                    conn = self.connections[conn_id]
                except KeyError:
                    sleep(0.5)
                    conn_id = self.tickers.get_sub_type_conn_id(ticker_name, SUB_TYPE_ORDERBOOK)
                else:
                    break
            self.tickers.set_snapshot_state(ticker_name, SNAPSHOT_QUEUED)
            ### EXPERIMENTAL ###
            try:
                logger.info(MSG_INFO_ORDER_BOOK_REQUESTED.format(SUB_TYPE_ORDERBOOK, ticker_name))
                update_invokes(self.invokes, conn, QUERY_EXCHANGE_STATE, ticker_name)
                conn.corehub.server.invoke(QUERY_EXCHANGE_STATE, ticker_name)
                self.tickers.set_snapshot_state(ticker_name, SNAPSHOT_SENT)
            except Exception as e:
                print(e)
                print('Failed to invoke snapshot query')
            ###
            # self.control_queue.put(SnapshotEvent(ticker_name, conn))

    async def _handle_order(self, order_event):
        msg = order_event.message
        ticker = msg['M']
        snapshot_state = self.tickers.get_snapshot_state(ticker)
        if snapshot_state in [SNAPSHOT_OFF, SNAPSHOT_QUEUED, SNAPSHOT_SENT]:
            self._init_backorder_queue(ticker, order_event)
        elif snapshot_state == SNAPSHOT_RCVD:
            if self._transfer_backorder_queue(ticker):
                self.tickers.set_snapshot_state(ticker, SNAPSHOT_ON)
        if self.tickers.get_snapshot_state(ticker) == SNAPSHOT_ON:
            self._sync_order_book(ticker, order_event.message)
            await self.on_orderbook(self.order_books[ticker])
            # self.orderbook_callback.on_change(self.order_books[ticker])

    def _assign_conn(self, ticker, sub_type):
        # Changed 0 to 1 because '_is_running' was made into an event so
        # essentially if 1 means that only '_is_running' is in the queue
        # and we can proceed.
        ### EXPERIMENTAL
        # while self.control_queue.unfinished_tasks > 1:
        #     sleep(0.2)
        ###
        conns = self.tickers.sort_by_callbacks()
        d = {}
        if sub_type == SUB_TYPE_TICKERUPDATE:
            # Check for connection with enabled 'CALLBACK_SUMMARY_DELTAS'
            for conn in conns.keys():
                if CALLBACK_SUMMARY_DELTAS in conns[conn]:
                    d.update({conns[conn]['{} count'.format(CALLBACK_EXCHANGE_DELTAS)]: conn})
            # and get the connection with the lowest number of tickers.
            if d:
                min_tickers = min(d.keys())
                conn_id = d[min_tickers]
                return [SubscribeInternalEvent(ticker, self.connections[conn_id], sub_type)]
            # No connection found with 'CALLBACK_SUMMARY_DELTAS'.
            # Get the connection with the lowest number of tickers.
            else:
                for conn in conns.keys():
                    d.update({conns[conn]['{} count'.format(CALLBACK_EXCHANGE_DELTAS)]: conn})
                min_tickers = min(d.keys())
                conn_id = d[min_tickers]
                return [SubscribeEvent(ticker, self.connections[conn_id], sub_type)]
        else:
            # If 'EXCHANGE_DELTAS' is enabled for the ticker
            # and the specific connection, we just need to find the
            # connection and enable the subscription state in order
            # to stop filtering the messages.
            for conn in conns.keys():
                try:
                    if ticker in conns[conn][CALLBACK_EXCHANGE_DELTAS]:
                        return [SubscribeInternalEvent(ticker, self.connections[conn], sub_type)]
                except KeyError:
                    break
            # If there is no active subscription for the ticker,
            # check if there is enough quota and add the subscription to
            # an existing connection.
            for conn in conns.keys():
                d.update({conns[conn]['{} count'.format(CALLBACK_EXCHANGE_DELTAS)]: conn})
            # Quick and dirty method for when the connection has no assigned subscriptions to it.
            try:
                min_tickers = min(d.keys())
                if min_tickers < self.max_tickers_per_conn:
                    conn_id = d[min_tickers]
                    return [SubscribeEvent(ticker, self.connections[conn_id], sub_type)]
                # The existing connections are in full capacity, create a new connection and subscribe.
                else:
                    obj = self._create_bittrex_connection([ticker])[0]
                    conn_event = ConnectEvent(obj[1])
                    sub_event = SubscribeEvent(ticker, obj[1], sub_type)
                    return [conn_event, sub_event]
            except ValueError:
                # Pick the first connection
                conn_id = list(self.connections)[0]
                event = SubscribeEvent(ticker, self.connections[conn_id], sub_type)
                return [event]

    def _is_no_subs_active(self):
        # Close the websocket if no active subscriptions remain.
        active_conns = self.tickers.sort_by_callbacks()
        if not active_conns:
            self.disconnect()
        else:
            # Check for non-active connections and close ONLY them.
            non_active = set(self.connections) - set(active_conns)
            if non_active:
                for conn in non_active:
                    logger.info('Connection {} has no active subscriptions. Closing it...'.format(conn))
                    conn_object = self.connections[conn]
                    disconnect_event = DisconnectEvent(conn_object)
                    self.control_queue.put(disconnect_event)

    # ==============
    # Public Methods
    # ==============

    # -----------------
    # Subscribe Methods
    # -----------------

    def subscribe_to_orderbook(self, tickers):
        """
        Subscribe and maintain the live order book for a set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        :param book_depth: The desired depth of the order book to be maintained.
        :type book_depth: int
        """
        event = IsFirstRunEvent(tickers, SUB_TYPE_ORDERBOOK)
        asyncio.Task(self.control_queue.put(event), loop=self.socket_loop)

    def subscribe_to_orderbook_update(self, tickers):
        """
        Subscribe to order book updates for a set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        event = IsFirstRunEvent(tickers, SUB_TYPE_ORDERBOOKUPDATE)
        asyncio.Task(self.control_queue.put(event), loop=self.socket_loop)
        # event = SubscribeEvent(tickers, None, SUB_TYPE_ORDERBOOKUPDATE)
        # asyncio.Task(self.control_queue.put(event), loop=self.socket_loop)

    def subscribe_to_trades(self, tickers):
        """
        Subscribe and receive tick data(executed trades) for a set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        sub_type = SUB_TYPE_TRADES
        self.control_queue.put(IsFirstRunEvent(tickers, sub_type))
        # if self._is_first_run(tickers, sub_type) is False:
        #     self._is_running(tickers, sub_type)

    def subscribe_to_ticker_update(self, tickers=None):
        """
        Subscribe and receive general data updates for a set of ticker(s). Example output:

        {
            'MarketName': 'BTC-ADA',
            'High': 7.65e-06,
            'Low': 4.78e-06,
            'Volume': 1352355429.5288217,
            'Last': 7.2e-06,
            'BaseVolume': 7937.59243908,
            'TimeStamp': '2017-11-28T15:02:17.7',
            'Bid': 7.2e-06,
            'Ask': 7.21e-06,
            'OpenBuyOrders': 4452,
            'OpenSellOrders': 3275,
            'PrevDay': 5.02e-06,
            'Created': '2017-09-29T07:01:58.873'
        }

        :param tickers: A list of tickers you are interested in.
        :type tickers: [] or None
        """
        if tickers is None:
            tickers = [ALL_TICKERS]
        sub_type = SUB_TYPE_TICKERUPDATE
        self.control_queue.put(IsFirstRunEvent(tickers, sub_type))
        # if self._is_first_run(tickers, sub_type) is False:
        #     self._is_running(tickers, sub_type)

    # -------------------
    # Unsubscribe Methods
    # -------------------

    def unsubscribe_from_orderbook(self, tickers, unsub_type=True):
        """
        Unsubscribe from real time order for specific set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        sub_type = SUB_TYPE_ORDERBOOK
        self._unsubscribe(tickers, sub_type, unsub_type)

    def unsubscribe_from_orderbook_update(self, tickers, unsub_type=True):
        """
        Unsubscribe from order book updates for a set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        sub_type = SUB_TYPE_ORDERBOOKUPDATE
        self._unsubscribe(tickers, sub_type, unsub_type)

    def unsubscribe_from_trades(self, tickers, unsub_type=True):
        """
        Unsubscribe from receiving tick data(executed trades) for a set of ticker(s)

        :param tickers: A list of tickers you are interested in.
        :type tickers: []
        """
        sub_type = SUB_TYPE_TRADES
        self._unsubscribe(tickers, sub_type, unsub_type)

    def unsubscribe_from_ticker_update(self, tickers=None, unsub_type=True):
        """
        Unsubscribe from receiving general data updates for a set of ticker(s).

        :param tickers: A list of tickers you are interested in.
        :type tickers: [] or None
        """
        if tickers is None:
            tickers = [ALL_TICKERS]
        sub_type = SUB_TYPE_TICKERUPDATE
        self._unsubscribe(tickers, sub_type, unsub_type)

    # -------------
    # Other Methods
    # -------------

    def get_order_book(self, ticker=None):
        """
        Returns the most recently updated order book for the specific ticker.
        If no ticker is specified, returns a dictionary with the order books of
        all subscribed tickers.

        :param ticker: The specific ticker you want the order book for.
        :type ticker: str
        """
        if ticker is None:
            return self.order_books
        else:
            return self.order_books[ticker]

    def get_order_book_sync_state(self, tickers=None):
        """
        Returns the sync state of the order book for the specific ticker(s).
        If no ticker is specified, returns the state for all tickers.
        The sync states are:

            Not initiated = 0
            Invoked, not synced = 1
            Received, not synced, not processing = 2
            Received, synced, processing = 3

        :param tickers: The specific ticker(s) and it's order book sync state you are interested in.
        :type tickers: []
        """
        if tickers is not None:
            t = find_ticker_type(tickers)
        else:
            t = self.tickers.list.keys()
        states = {}
        for ticker in t:
            if self.tickers.get_sub_state(ticker, SUB_TYPE_ORDERBOOK) is True:
                state = self.tickers.get_snapshot_state(ticker)
                states[ticker] = state
        return states

    def disconnect(self):
        """
        Disconnects the connections and stops the websocket instance.
        """
        self.control_queue.put(DisconnectEvent())

    @staticmethod
    def enable_log(file_name=None):
        """
        Enables logging.
        :param file_name: The name of the log file, located in the same directory as the executing script.
        :type file_name: str
        """
        add_stream_logger(file_name=file_name)

    @staticmethod
    def disable_log():
        """
        Disables logging.
        """
        remove_stream_logger()

    def _create_bittrex_connection(self, tickers):
        results = []

        def get_chunks(l, n):
            # Yield successive n-sized chunks from l.
            for i in range(0, len(l), n):
                yield l[i:i + n]

        ticker_gen = get_chunks(list(tickers), self.max_tickers_per_conn)
        # Initiate a generator that splits the ticker list into chunks
        while True:
            try:
                chunk_list = next(ticker_gen)
            except StopIteration:
                break
            if chunk_list is not None:
                conn_obj = self._setup_bittrex_connection()
                results.append([chunk_list, conn_obj])

        return results

    def _setup_bittrex_connection(self):
        connection = Connection('https://beta.bittrex.com/signalr')
        hub = connection.register_hub('c2')
        connection.received += self._on_debug
        connection.error += self.on_error
        # Market delta callback
        hub.client.on('uE', self._on_tick_update)
        # Summary + lite summary delta callbacks
        hub.client.on('uS', self._on_ticker_update)
        hub.client.on('uL', self._on_ticker_update)

        return BittrexConnection(connection, hub, self.max_tickers_per_conn)

    async def _is_orderbook_snapshot(self, msg):
        # Detect if the message contains order book snapshots and manipulate them.
        if 'R' in msg and type(msg['R']) is not bool:
            msg_snapshot = process_message(msg['R'])
            if 'M' in msg_snapshot and msg_snapshot['M'] is None:
                snapshot_event = SnapshotEvent(msg_snapshot, int(msg['I']))
                asyncio.Task(self.control_queue.put(snapshot_event), loop=self.socket_loop)

    async def _handle_snapshot(self, snapshot_event):
        msg = snapshot_event.message
        counter = snapshot_event.counter
        if self.invokes[counter]['invoke'] == QUERY_EXCHANGE_STATE:
            msg['M'] = self.invokes[counter]['ticker']
            del msg['f']
            self.order_books[msg['M']] = msg
            self.tickers.set_snapshot_state(msg['M'], SNAPSHOT_RCVD)
        else:
            raise NotImplementedError('Please report error to '
                                      'https://github.com/slazarov/python-bittrex-websocket, '
                                      'Error:_handle_snapshot')
        logger.info(NSG_INFO_ORDER_BOOK_RECEIVED.format(SUB_TYPE_ORDERBOOK, msg['M']))

    def _init_backorder_queue(self, ticker, msg):
        sub = self.tickers.list[ticker][SUB_TYPE_ORDERBOOK]
        if sub['InternalQueue'] is None:
            sub['InternalQueue'] = deque()
        sub['InternalQueue'].append(msg.message)
        self.tickers.increment_nounces(ticker)

    def _transfer_backorder_queue(self, ticker):
        sub = self.tickers.list[ticker][SUB_TYPE_ORDERBOOK]
        q = sub['InternalQueue']
        while True:
            try:
                e = q[0]
            except IndexError:
                sub['InternalQueue'] = None
                return True
            except AttributeError:
                raise NotImplementedError('Please report error to '
                                          'https://github.com/slazarov/python-bittrex-websocket, '
                                          'Error:_transfer_backorder_queue:AttributeError')
            else:
                if self._sync_order_book(ticker, e):
                    self.tickers.set_snapshot_state(ticker, SNAPSHOT_ON)
                q.pop()

    def _transfer_backorder_queue2(self, ticker, snapshot):
        confirmed = False
        sub = self.tickers.list[ticker][SUB_TYPE_ORDERBOOK]
        q = sub['InternalQueue']
        q2 = deque()
        while True:
            try:
                e = q[0]
                q2.append(e)
            except IndexError:
                sub['InternalQueue'] = q2
                return confirmed
            except TypeError:
                return confirmed
            except AttributeError:
                raise NotImplementedError('Please report error to '
                                          'https://github.com/slazarov/python-bittrex-websocket, '
                                          'Error:_transfer_backorder_queue:AttributeError')
            else:
                if self._confirm_order_book(snapshot, e):
                    confirmed = True
                q.pop()

    # ========================
    # Private Channels Methods
    # ========================

    async def _on_debug(self, **kwargs):
        """
        Debug information, shows all data
        Don't edit unless you know what you are doing.
        Redirect full order book snapshots to on_message
        """
        # print(process_message(kwargs))
        # if self._is_close_me():
        #     return
        await self._is_orderbook_snapshot(kwargs)

    async def _on_tick_update(self, args):
        # if self._is_close_me():
        #     return
        msg = process_message(args[0])
        ticker = msg['M']
        if self.tickers.get_sub_state(ticker, SUB_TYPE_ORDERBOOK) is SUB_STATE_ON:
            if self.tickers.get_snapshot_state(ticker) is SNAPSHOT_OFF:
                self._get_snapshot([ticker])
            await asyncio.Task(self.control_queue.put(OrderEvent(msg)), loop=self.socket_loop)
        if self.tickers.get_sub_state(ticker, SUB_TYPE_ORDERBOOKUPDATE) is SUB_STATE_ON:
            d = dict(self._create_base_layout(msg),
                     **{'bids': msg['Z'],
                        'asks': msg['S']})
            await self.on_orderbook_update(d)
        # if self.tickers.get_sub_state(ticker, SUB_TYPE_TRADES) is SUB_STATE_ON:
        #     if msg['Fills']:
        #         d = dict(self._create_base_layout(msg),
        #                  **{'trades': msg['Fills']})
        #         self.trades.on_change(d)

    async def _on_ticker_update(self, args):
        """
        Invoking summary state updates for specific filter
        doesn't work right now. So we will filter them manually.
        """
        # if self._is_close_me():
        #     return
        msg = process_message(args[0])
        if 'Deltas' in msg:
            for update in msg['D']:
                pass
                # if self.tickers.get_sub_state(ALL_TICKERS, SUB_TYPE_TICKERUPDATE) is SUB_STATE_ON:
                #     self.updateSummaryState.on_change(msg['Deltas'])
                # else:
                #     try:
                #         ticker = update['MarketName']
                #         subs = self.tickers.get_ticker_subs(ticker)
                #     except KeyError:  # not in the subscription list
                #         continue
                #     else:
                #         if subs['TickerUpdate']['Active']:
                #             self.updateSummaryState.on_change(update)

    # -------------------------------------
    # Private Channels Supplemental Methods
    # -------------------------------------

    @staticmethod
    def _create_base_layout(msg):
        d = {'ticker': msg['M'],
             'nounce': msg['N'],
             'timestamp': time()
             }
        return d

    def _sync_order_book(self, ticker, order_data):
        # Syncs the order book for the pair, given the most recent data from the socket
        book_depth = self.tickers.list[ticker][SUB_TYPE_ORDERBOOK]
        nounce_diff = order_data['N'] - self.order_books[ticker]['N']
        if nounce_diff == 1:
            self.order_books[ticker]['N'] = order_data['N']
            # Start syncing
            for side in [['Z', True], ['S', False]]:
                made_change = False

                for item in order_data[side[0]]:
                    # TYPE 0: New order entries at matching price
                    # -> ADD to order book
                    if item['TY'] == 0:
                        self.order_books[ticker][side[0]].append(
                            {
                                'Q': item['Q'],
                                'R': item['R']
                            })
                        made_change = True

                    # TYPE 1: Cancelled / filled order entries at matching price
                    # -> DELETE from the order book
                    elif item['TY'] == 1:
                        for i, existing_order in enumerate(self.order_books[ticker][side[0]]):
                            if existing_order['R'] == item['R']:
                                del self.order_books[ticker][side[0]][i]
                                # made_change = True
                                break

                    # TYPE 2: Changed order entries at matching price (partial fills, cancellations)
                    # -> EDIT the order book
                    elif item['TY'] == 2:
                        for existing_order in self.order_books[ticker][side[0]]:
                            if existing_order['R'] == item['R']:
                                existing_order['Q'] = item['Q']
                                #made_change = True
                                break

                if made_change:
                    # Sort by price, with respect to BUY(desc) or SELL(asc)
                    self.order_books[ticker][side[0]] = sorted(
                        self.order_books[ticker][side[0]],
                        key=lambda k: k['R'],
                        reverse=side[1])
                    # Add nounce unix timestamp
                    self.order_books[ticker]['timestamp'] = time()
            return True
        # The next nounce will trigger a sync.
        elif nounce_diff == 0:
            return True
        # The order book snapshot nounce is ahead. Discard this nounce.
        elif nounce_diff < 0:
            return False
        else:
            # Experimental resync
            logger.error(
                '[Subscription][{}][{}]: Out of sync. Trying to resync...'.format(SUB_TYPE_ORDERBOOK, ticker))
            # self.tickers.disable(ticker, SUB_TYPE_ORDERBOOK)
            self.tickers.change_sub_state(ticker, SUB_TYPE_ORDERBOOK, SUB_STATE_OFF)
            # self.control_queue.put(ResyncEvent(ticker, SUB_TYPE_ORDERBOOK, book_depth))
            # self._handle_reconnect([ticker], SUB_TYPE_ORDERBOOK, book_depth)
            event = ReconnectEvent([ticker], SUB_TYPE_ORDERBOOK, book_depth)
            self.control_queue.put(event)

    def _confirm_order_book(self, snapshot, nounce_data):
        # Syncs the order book for the pair, given the most recent data from the socket
        nounce_diff = nounce_data['N'] - snapshot['N']
        if nounce_diff == 1:
            # Start confirming
            for side in [['Buys', True], ['Sells', False]]:
                made_change = False
                for item in nounce_data[side[0]]:
                    # TYPE 1: Cancelled / filled order entries at matching price
                    # -> DELETE from the order book
                    if item['Type'] == 1:
                        for i, existing_order in enumerate(
                                self.order_books[snapshot][side[0]]):
                            if existing_order['Rate'] == item['Rate']:
                                del self.order_books[snapshot][side[0]][i]
                                made_change = True
                                break

                    # TYPE 2: Changed order entries at matching price (partial fills, cancellations)
                    # -> EDIT the order book
                    elif item['Type'] == 2:
                        for existing_order in self.order_books[snapshot][side[0]]:
                            if existing_order['Rate'] == item['Rate']:
                                existing_order['Quantity'] = item['Quantity']
                                made_change = True
                                break
                if made_change:
                    return True
                else:
                    return False
        # The next nounce will trigger a sync.
        elif nounce_diff == 0:
            return True
        # The order book snapshot nounce is ahead. Discard this nounce.
        elif nounce_diff < 0:
            return False

    def _is_close_me(self):
        thread_name = current_thread().getName()
        conn_object = self._return_conn_by_thread_name(thread_name)
        if conn_object.close_me:
            try:
                conn_object.conn.close()
            except WebSocketConnectionClosedException:
                pass
            conn_object.deactivate()
            return True

    def _return_conn_by_thread_name(self, thread_name):
        for conn in self.connections:
            if self.connections[conn].thread_name == thread_name:
                return self.connections[conn]

    # ===============
    # Public Channels
    # ===============

    def on_open(self):
        # Called before initiating the first websocket connection
        # Use it when you want to add some opening logic.
        pass

    def on_close(self):
        # Called before closing the websocket instance.
        # Use it when you want to add any closing logic.
        # print('Bittrex websocket closed.')
        pass

    async def on_error(self, error):
        # Error handler
        print(error)
        # self.disconnect()

    async def on_orderbook(self, msg):
        pass

    async def on_orderbook_update(self, msg):
        # The main channel of subscribe_to_orderbook_update().
        # print('[OrderBookUpdate]: {}'.format(msg['ticker']))
        pass

    async def on_trades(self, msg):
        # The main channel of subscribe_to_trades().
        # print('[Trades]: {}'.format(msg['ticker']))
        pass

    def on_ticker_update(self, msg):
        # The main channel of subscribe_to_ticker_update().
        # print('Just received ticker update for {}.'.format(msg['MarketName']))
        pass
