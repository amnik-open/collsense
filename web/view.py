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
                    </style>
                    <body>
                    {result}
                    </body>
                    </html>'''
        return report
    @staticmethod
    def _create_html_section(head, rows):
        if rows != "":
            output = f'''<h2>{head}</h2>
    
                        <table style="width:100%">
                          <tr>
                            <th>Sensor</th>
                            <th>Parameter</th>
                            <th>Mean</th>
                          </tr>
                          {rows}
                        </table>
                        '''
        else:
            output = f'''<h2>{head}</h2>
                        <p>No data now</p>
                      '''
        return output

    @staticmethod
    def _create_html_table_rows(sensor, parameter, mean):
        output = f'''<tr>
                    <td>{sensor}</td>
                    <td>{parameter}</td>
                    <td>{mean}</td>
                    </tr>
                    '''
        return output

    def report_mean(self):
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
            result += self._create_html_section(head=f"last {mean} Mean",
                                               rows=rows)
        output = self._create_html_report(result)
        return output
