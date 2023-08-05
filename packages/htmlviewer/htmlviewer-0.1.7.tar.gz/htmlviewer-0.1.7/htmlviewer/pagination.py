from IPython.display import display
import math

from .core import view_table


class PagedViewer:
    chunk_size = 10
    page_number = 0

    def __init__(self,
                 records,
                 chunk_size=10,
                 **kwargs):
        self.records = list(records)
        self.chunk_size = chunk_size
        self.viewer_kwargs = kwargs

    @property
    def page_count(self):
        return math.ceil(self.record_count / self.chunk_size)

    @property
    def record_count(self):
        return len(self.records)

    def __len__(self):
        return self.record_count

    def _repr_html_(self):
        display(self.view())
        return ''

    def view(self, page_number=None, start=None):
        """Choose a page number to view

        Keyword Arguments:
            page_number {int >= -1} -- Page number to view (default: {self.page_number})
            start {int} -- Sequence of the record to start viewing (default: {None})

        Returns:
            Viewer function object
        """

        if page_number is None:
            page_number = self.page_number
        elif page_number == -1:
            page_number = self.page_count - 1

        self.page_number = page_number

        if start is None:
            start = page_number * self.chunk_size

        return view_table(self.records[start: start + self.chunk_size], **self.viewer_kwargs)

    def next(self):
        """Shows the next page

        Returns:
            Viewer function object
        """

        if len(self.records) < (self.page_number + 1) * self.chunk_size:
            self.page_number = 0
        else:
            self.page_number += 1

        return self.view()

    def previous(self):
        """Show the previous page

        Returns:
            Viewer function object
        """

        self.page_number -= 1
        if self.page_number < 0:
            self.page_number = self.page_count - 1

        return self.view()

    def first(self):
        """Shows the first page

        Returns:
            Viewer function object
        """

        return self.view(0)

    def last(self):
        """Shows the last page

        Returns:
            Viewer function object
        """

        return self.view(-1)
