from flask import send_file
from flask_restplus import Resource

from ..service.doms_service import get_all_domains
from ..service.file_service import generate_typhoon_report
from ..util.dto import TyphonnDto
from ...spiders.agoraspider import AgoraSpdier
from ...spiders.jmpaspider import JMASpdier
from ...spiders.listTyphoonsByYear import TyphoonSearchSpider

api = TyphonnDto.api
simple = TyphonnDto.simple


@api.route('/')
class TyphonnsList(Resource):
    """
        Domain Resource
    """
    @api.doc('Get All Domains')
    @api.marshal_list_with(simple)
    def get(self):
        return get_all_domains()


@api.route('/<id>/tracking')
class TyphoonTracking(Resource):
    """
        Domain Resource
    """
    @api.doc('Get All Domains')
    # @api.marshal_list_with(simple)
    def get(self, id):
        spider = AgoraSpdier()
        spider.execute(name=id)
        return spider.reports


@api.route('/search/year/<year>')
class TyphoonTracking(Resource):
    """
        Domain Resource
    """
    @api.doc('Get All Domains')
    # @api.marshal_list_with(simple)
    def get(self, year):
        spider = TyphoonSearchSpider()
        spider.execute(year=year)
        return spider.reports


@api.route('/current')
class CurrentTyphonn(Resource):
    """
        Domain Resource
    """
    # @api.doc('Get All Domains')
    # @api.marshal_list_with(simple)
    def get(self):
        spider = JMASpdier()
        spider.execute()
        return spider.reports


@api.route('/<id>/file')
class TyphoonReport(Resource):
    """
        Domain Resource
    """
    # @api.doc('Get All Domains')
    # @api.marshal_list_with(simple)
    def get(self, id):
        spider = AgoraSpdier()
        spider.execute(name=id)
        tracking_info = spider.reports
        # tracking_info = None
        report_file_path = generate_typhoon_report(tracking_info)

        filename = 'export.xlsx'
        # AFTER THIS REQUEST DELETE TMP_FILE
        return send_file(report_file_path, as_attachment=True, attachment_filename=filename)