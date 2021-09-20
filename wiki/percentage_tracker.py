from PySide6.QtCore import Signal, QObject


class PercentageTracker(QObject):
    updated = Signal(int)

    def __init__(self, steps):
        QObject.__init__(self)
        self.steps = steps
        self.completed = 0

    def next(self):
        self.completed += 1
        self.updated.emit((self.completed/self.steps))

    def _receive_sub_update(self, amount):
        self.updated.emit((self.completed/self.steps) + (amount/self.steps))

    def segment(self, steps):
        segment_tracker = PercentageTracker(steps)
        segment_tracker.updated.connect(self._receive_sub_update)
        return segment_tracker
