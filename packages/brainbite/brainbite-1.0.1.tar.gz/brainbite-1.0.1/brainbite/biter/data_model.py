import sys


class BFDataModel:
    """
    This holds cells what behaves as the Turing Machine's tape.
    """

    def __init__(self, size=30000):
        self._data = [0 for _ in range(size)]
        self._index = 0

    @property
    def pointer(self):
        return self._index

    @pointer.setter
    def pointer(self, value):
        self._index = value % len(self._data)

    @property
    def pointee(self):
        return self._data[self._index]

    @pointee.setter
    def pointee(self, value):
        self._data[self._index] = value

    def increment_pointer(self):
        """This corresponds to operation '>'."""
        self.pointer += 1

    def decrement_pointer(self):
        """This corresponds to operation '<'."""
        self.pointer -= 1

    def increment_pointee(self):
        """This corresponds to operation '+'."""
        self.pointee += 1

    def decrement_pointee(self):
        """This corresponds to operation '-'."""
        self.pointee -= 1

    def conditional_skip(self) -> bool:
        """This corresponds to operation '['."""
        return self.pointee == 0

    def unconditional_jump(self):
        """This corresponds to operation ']'."""
        pass

    def print_pointee(self):
        """This corresponds to operation '.'."""
        sys.stdout.write(
            chr(self.pointee)
        )

    def input_to_pointee(self):
        """This corresponds to operation ','."""
        self.pointee = ord(sys.stdin.read(1))
