"""Event bus for SceneSense with metrics and diagnostics."""

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from app.logger.logger import Logger


@dataclass
class EventMetrics:
    """Track metrics for events published through the event bus."""

    event_name: str
    publish_count: int = 0
    total_publish_time_ms: float = 0.0
    subscribers_count: int = 0
    last_publish_time: Optional[float] = None
    average_publish_time_ms: float = 0.0


@dataclass
class EventMetricsSnapshot:
    """Snapshot of all event metrics for diagnostics."""

    events: Dict[str, EventMetrics] = field(default_factory=dict)
    total_events_published: int = 0
    longest_event_name: str = ""
    highest_publish_count_event: str = ""

    def __str__(self) -> str:
        return f"EventMetricsSnapshot(events={list(self.events.keys())}, total={self.total_events_published})"


class EventBus:
    """Thread-safe event bus with metrics collection."""

    def __init__(self, logger: Optional[Logger] = None):
        self._subscribers: Dict[str, List[Callable]] = {}
        self.logger = logger or Logger("app.events.event_bus")
        self._metrics_history: List[EventMetricsSnapshot] = deque(maxlen=100)  # Keep last 100 snapshots

    def subscribe(self, event_name: str, callback: Callable) -> int:
        """
        Subscribe to an event.

        Args:
            event_name: Name of the event to subscribe to
            callback: Callback function to invoke when event is published

        Returns:
            Subscriber ID for unsubscribing later
        """
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
            self.logger.debug(f"Registered new event type: {event_name}")

        subscriber_id = len(self._subscribers[event_name])
        self._subscribers[event_name].append(callback)

        # Update metrics
        if event_name not in self._metrics:
            self._metrics[event_name] = EventMetrics(event_name=event_name)
        self._metrics[event_name].subscribers_count += 1

        self.logger.debug(f"Subscribed to '{event_name}' (subscribers: {len(self._subscribers[event_name])})")
        return subscriber_id

    def unsubscribe(self, event_name: str, subscriber_id: int) -> bool:
        """
        Unsubscribe from an event.

        Args:
            event_name: Name of the event to unsubscribe from
            subscriber_id: Subscriber ID returned from subscribe()

        Returns:
            True if unsubscribed successfully, False otherwise
        """
        if event_name in self._subscribers and subscriber_id < len(self._subscribers[event_name]):
            removed = self._subscribers[event_name].pop(subscriber_id)
            self.logger.debug(f"Unsubscribed from '{event_name}' (removed {removed.__name__ if hasattr(removed, '__name__') else 'callback'})")
            return True
        return False

    def publish(self, event_name: str, data: dict, metrics: bool = True) -> Optional[str]:
        """
        Publish an event to all subscribers.

        Args:
            event_name: Name of the event
            data: Event data dictionary
            metrics: Whether to record timing metrics (default: True)

        Returns:
            None if success, or error message string if failed
        """
        start_time = time.perf_counter()

        if event_name not in self._subscribers:
            self.logger.warning(f"No subscribers for event '{event_name}'")
            return f"Event '{event_name}' has no subscribers"

        subscribers = self._subscribers[event_name]
        error_messages = []

        for subscriber in subscribers:
            try:
                subscriber(data)
            except Exception as e:
                error_msg = f"Subscriber {subscriber.__name__ if hasattr(subscriber, '__name__') else repr(subscriber)} failed: {e}"
                self.logger.error(error_msg)
                error_messages.append(error_msg)

        end_time = time.perf_counter()
        publish_time_ms = (end_time - start_time) * 1000

        # Record metrics if enabled
        if metrics and event_name in self._metrics:
            self._metrics[event_name].publish_count += 1
            self._metrics[event_name].total_publish_time_ms += publish_time_ms
            self._metrics[event_name].average_publish_time_ms = (
                self._metrics[event_name].total_publish_time_ms / self._metrics[event_name].publish_count
                if self._metrics[event_name].publish_count > 0 else 0.0
            )
            self._metrics[event_name].last_publish_time = end_time

        # Log event if DEBUG level enabled
        if self.logger.level <= logging.DEBUG:
            method = getattr(self, "_last_method", "unknown") if hasattr(self, "_last_method") else "unknown"
            duration_ms = getattr(data, "duration_ms", "<1ms") if isinstance(data, dict) and "duration_ms" in data else publish_time_ms
            self.logger.debug(
                f"Event '{event_name}' published to {len(subscribers)} subscriber(s) - {publish_time_ms:.3f}ms ({method})",
                extra={
                    "event_name": event_name,
                    "subscribers_count": len(subscribers),
                    "duration_ms": publish_time_ms,
                },
            )

        if error_messages:
            return "; ".join(error_messages)
        return None

    def get_metrics_snapshot(self) -> EventMetricsSnapshot:
        """Get current snapshot of all event metrics."""
        events = {}
        total_events = 0
        longest_name = ""
        highest_count_event = ""

        for name, metrics in self._metrics.items():
            events[name] = metrics
            total_events += metrics.publish_count
            if len(name) > len(longest_name):
                longest_name = name
            if metrics.publish_count > 0 and (highest_count_event == "" or metrics.publish_count > self.get_max_publish_count()):
                highest_count_event = name

        snapshot = EventMetricsSnapshot(
            events=events,
            total_events_published=total_events,
            longest_event_name=longest_name,
            highest_publish_count_event=highest_count_event,
        )

        # Store in history for trend analysis
        self._metrics_history.append(snapshot)

        return snapshot

    def get_metrics(self, event_name: Optional[str] = None) -> dict:
        """Get detailed metrics for an event (or all events if no name specified)."""
        if event_name is None:
            all_events = {}
            for name, metrics in self._metrics.items():
                all_events[name] = {
                    "publish_count": metrics.publish_count,
                    "average_publish_time_ms": metrics.average_publish_time_ms,
                    "subscribers_count": metrics.subscribers_count,
                    "total_publish_time_ms": metrics.total_publish_time_ms,
                }
            return {"all_events": all_events, "total_events_published": sum(m.publish_count for m in self._metrics.values())}

        if event_name in self._metrics:
            metrics = self._metrics[event_name]
            return {
                "event_name": event_name,
                "publish_count": metrics.publish_count,
                "average_publish_time_ms": metrics.average_publish_time_ms,
                "subscribers_count": metrics.subscribers_count,
                "total_publish_time_ms": metrics.total_publish_time_ms,
                "last_publish_time": metrics.last_publish_time.isoformat() if metrics.last_publish_time else None,
            }

        return {"error": f"Event '{event_name}' not found"}

    def clear_metrics(self):
        """Clear all event metrics (useful for testing)."""
        self._metrics = {}
        self.logger.debug("Cleared all event metrics")

    @property
    def metrics(self) -> Dict[str, EventMetrics]:
        """Get copy of current metrics dictionary."""
        return dict(self._metrics) if hasattr(self, '_metrics') else {}


# Store in module level for easy access
event_bus_instance: Optional[EventBus] = None


def get_event_bus(logger: Optional[Logger] = None) -> EventBus:
    """Get or create the global event bus instance."""
    global event_bus_instance
    if event_bus_instance is None:
        event_bus_instance = EventBus(logger=logger)
    return event_bus_instance
