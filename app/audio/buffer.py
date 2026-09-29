import queue

class AudioBuffer:
    """Thread-safe buffer for audio chunks."""
    def __init__(self, maxsize=0):
        self._queue = queue.Queue(maxsize=maxsize)
        
    def put(self, chunk):
        """Put a chunk of audio into the buffer."""
        self._queue.put(chunk)
        
    def get(self, block=True, timeout=None):
        """Get a chunk of audio from the buffer."""
        return self._queue.get(block=block, timeout=timeout)
        
    def clear(self):
        """Clear all chunks from the buffer."""
        with self._queue.mutex:
            self._queue.queue.clear()
            
    def empty(self):
        """Check if the buffer is empty."""
        return self._queue.empty()
