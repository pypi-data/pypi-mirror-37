import os
import pickle
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileCreatedEvent, FileDeletedEvent, FileModifiedEvent, FileMovedEvent, \
    DirCreatedEvent, DirDeletedEvent, DirModifiedEvent, DirMovedEvent
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
import logging
from watchdog.events import LoggingEventHandler


class _EmptySnapshot(DirectorySnapshot):
    @property
    def stat_snapshot(self):
        return dict()

    @property
    def paths(self):
        return set()


class PersistantObserver(Observer):
    def __init__(self, *args, **kwargs):
        """
        Check if watching folders has changed since last observation.
        If change detected, emit corresponding events at suscribers handlers.
        At the `Observer.stop`, save states of folders with pickle for the next observation.
        PARAMETERS
        ==========
        save_to : unicode
            path where save pickle dumping
        protocol (optionnal): int
            protocol used for dump current states of watching folders
        """
        self._filename = kwargs.pop('save_to')
        self._protocol = kwargs.pop('protocol', 0)
        Observer.__init__(self, *args, **kwargs)

    def start(self, *args, **kwargs):
        previous_snapshots = dict()
        if os.path.exists(self._filename):
            with open(self._filename, 'rb') as f:
                previous_snapshots = pickle.load(f)

        for watcher, handlers in self._handlers.items():
            try:
                path = watcher.path
                curr_snap = DirectorySnapshot(path)
                pre_snap = previous_snapshots.get(path, _EmptySnapshot(path))
                diff = DirectorySnapshotDiff(pre_snap, curr_snap)
                for handler in handlers:
                    # Dispatch files modifications
                    for new_path in diff.files_created:
                        handler.dispatch(FileCreatedEvent(new_path))
                    for del_path in diff.files_deleted:
                        handler.dispatch(FileDeletedEvent(del_path))
                    for mod_path in diff.files_modified:
                        handler.dispatch(FileModifiedEvent(mod_path))
                    for src_path, mov_path in diff.files_moved:
                        handler.dispatch(FileMovedEvent(src_path, mov_path))

                    # Dispatch directories modifications
                    for new_dir in diff.dirs_created:
                        handler.dispatch(DirCreatedEvent(new_dir))
                    for del_dir in diff.dirs_deleted:
                        handler.dispatch(DirDeletedEvent(del_dir))
                    for mod_dir in diff.dirs_modified:
                        handler.dispatch(DirModifiedEvent(mod_dir))
                    for src_path, mov_path in diff.dirs_moved:
                        handler.dispatch(DirMovedEvent(src_path, mov_path))
            except PermissionError as e:
                print(e)

        Observer.start(self, *args, **kwargs)

    def stop(self, *args, **kwargs):
        try:
            snapshots = {handler.path: DirectorySnapshot(handler.path) for handler in self._handlers.keys()}
            with open(self._filename, 'wb') as f:
                pickle.dump(snapshots, f, self._protocol)
            Observer.stop(self, *args, **kwargs)
        except PermissionError as e:
            print(e)


def observe_realtime(path=os.path.curdir):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def observe_over_sessions(path=os.path.curdir):
    logging.basicConfig(level=logging.DEBUG)
    event_handler = LoggingEventHandler()
    observer = PersistantObserver(save_to='C:\\temp\\test.pickle', protocol=-1)
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    # observer.join()
    observer.stop()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def compare_dirs(src_path, dest_path):
    src_snap = DirectorySnapshot(src_path)
    dest_path = DirectorySnapshot(dest_path)
    diff = DirectorySnapshotDiff(src_snap, dest_path)
    print(diff.files_modified)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # observe_realtime(path)
    # observe_over_sessions(path)
    compare_dirs("C:\\New folder\\temp", "C:\\temp")
