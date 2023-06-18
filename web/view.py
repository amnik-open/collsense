from db.tsdb_interface import InfluxdbInterface
from config.config import CollsenseConfig

Conf = CollsenseConfig()


class CollsenseView:

    def __init__(self):
        self.db = InfluxdbInterface()

    @staticmethod
    def _create_html_report(result):
        report = f'''<html>
                    <style>
                    table, th, td {{
                      border:1px solid black;
                    }}
                    td {{
                      text-align: center;
                      vertical-align: middle;
                    }}
                    </style>
                    <body>
                    {result}
                    </body>
                    </html>'''
        return report

    @staticmethod
    def _create_html_section(head, table_head, rows, message="No data now"):
        if rows != "":
            output = f'''<h2>{head}</h2>
    
                        <table style="width:100%">
                          {table_head}
                          {rows}
                        </table>
                        '''
        else:
            output = f'''<h2>{head}</h2>
                        <p>{message}</p>
                      '''
        return output

    @staticmethod
    def _create_html_table_rows(data1, data2, data3):
        output = f'''<tr>
                    <td>{data1}</td>
                    <td>{data2}</td>
                    <td>{data3}</td>
                    </tr>
                    '''
        return output

    @staticmethod
    def _create_html_table_head(head1, head2, head3):
        output = f'''<tr>
                    <th>{head1}</td>
                    <th>{head2}</td>
                    <th>{head3}</td>
                    </tr>
                    '''
        return output

    def _create_mean_report(self):
        means = Conf.get_collector_config()["tasks_mean_period"].split(",")
        columns = ['_measurement', '_field', '_value']
        result = ""
        for mean in means:
            mean = mean.strip()
            mean_rows = self.db.query_bucket(bucket=f"{mean}_mean",
                                             range=f"-{mean}",
                                             columns=columns, last=True)
            rows = ""
            for row in mean_rows:
                rows += self._create_html_table_rows(row[0], row[1], row[2])
            table_head = self._create_html_table_head("Sensor", "Parameter",
                                                      "Mean")
            result += self._create_html_section(head=f"last {mean} Mean",
                                                table_head=table_head,
                                                rows=rows)
        return result

    def _create_undefined_sensor_report(self):
        bucket = Conf.get_database_config()['bucket']
        columns = ['_time', 'url', 'status']
        undefined_sensor_rows = self.db.query_bucket(bucket=bucket, range='0',
                                                columns=columns, last=False,
                                                measurement='undefined_sensor')
        result = ""
        rows = ""
        for row in undefined_sensor_rows:
            rows += self._create_html_table_rows(row[0], row[1], row[2])
        table_head = self._create_html_table_head("Time", "URL",
                                                  "Status")
        result += self._create_html_section(head=f"Undefined Sensors",
                                            table_head=table_head,
                                            rows=rows, message="No Sensor")
        return result

    def report(self):
        m_report = self._create_mean_report()
        u_report = self._create_undefined_sensor_report()
        report = m_report + u_report
        output = self._create_html_report(report)
        return output
