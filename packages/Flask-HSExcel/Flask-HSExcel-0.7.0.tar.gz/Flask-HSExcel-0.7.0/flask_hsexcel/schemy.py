import xlwt, time, random, os
from flask import current_app, make_response, send_file
from urllib.parse import quote
from marshmallow import Schema, fields, post_dump
from collections import defaultdict, OrderedDict


class ExcleSchema(Schema):
    excel_id = fields.Integer()
    name = fields.String()
    import_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    status = fields.Integer()
    excel_type = fields.String()
    extend = fields.String()


class ExcelExportSchema(Schema):
    class Meta:
        ordered = True

    @post_dump(pass_many=True)
    def data_excel(self, data, many):
        data_dict = defaultdict(list)
        for i in data:
            for k, v in i.items():
                data_dict[k].append(v)
        data_dict = OrderedDict(sorted(data_dict.items(), key=lambda x: x[0][0]))
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('导出结果')
        n = 0
        for k, v in data_dict.items():
            worksheet.write(0, n, k[1:])
            m = 1
            for i in v:
                worksheet.write(m, n, i)
                m = m + 1
            n = n + 1
        time_str = str(time.time())
        random_str = str(random.randint(1, 10000))
        file_name = time_str + random_str + '.xls'
        file_path = os.path.join(current_app.config['EXCEL_PATH'], file_name)
        workbook.save(file_path)
        response = make_response(send_file(file_path))
        basename = os.path.basename(self.context['file_name'])
        response.headers["Content-Disposition"] = \
            "attachment;" \
            "filename*=UTF-8''{utf_filename}".format(
                utf_filename=quote(basename.encode('utf-8'))
            )
        os.remove(file_path)
        return response
