from sqlalchemy.orm import Bundle


class DictBundle(Bundle):
    def create_row_processor(self, query, procs, labels):
        """Override create_row_processor to return values as
        dictionaries"""

        def proc(row):
            return dict(zip(labels, (proc(row) for proc in procs), strict=True))

        return proc
