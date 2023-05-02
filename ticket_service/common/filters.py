import arrow


class DateRangeBaseFilter:
    def get_date_time(self, value):
        return arrow.get(value, "YYYY-M-D h:m:s").datetime

    def get_range_start_date(self, value):
        return self.get_date_time("{} 0:0:0".format(value))

    def get_range_end_date(self, value):
        return self.get_date_time("{} 23:59:59".format(value))

    def convert_param(self, name, value, expr="gte"):
        param = {}
        param["{}__{}".format(name, expr)] = value
        return param

    def start_range(self, queryset, name, value):
        return queryset.filter(
            **self.convert_param(name, self.get_range_start_date(value))
        )

    def end_range(self, queryset, name, value):
        return queryset.filter(
            **self.convert_param(name, self.get_range_end_date(value), "lte")
        )
