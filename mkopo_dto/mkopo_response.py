import graphene
import json
import os


class ResponseObjects(graphene.ObjectType):
    id = graphene.String()
    status = graphene.Boolean()
    code = graphene.Int()
    message = graphene.String()

    @staticmethod
    def __read_code_file(code_id):
        current_dir = os.path.dirname(__file__)
        response_dir = os.path.join(current_dir, '..', 'openspace_assets')
        file_path = os.path.join(response_dir, 'response.json')
        # print(f"Trying to open file: {file_path}")
        file = open(file_path,'r',encoding='utf-8')
        file_codes = file.read()
        response_codes = json.loads(file_codes)
        response_code = next(code for code in response_codes if code["id"] == code_id)
        return response_code

    @staticmethod
    def get_response(id , message=None):
            response_code = ResponseObjects.__read_code_file(id)
            return ResponseObjects(
                id = response_code['id'],
                status = response_code['status'],
                code = response_code['code'],
                message = response_code['message'] if message is None else message ,
            )
            
class PageObject(graphene.ObjectType):
    number = graphene.Int()
    has_next_page = graphene.Boolean()
    has_previous_page = graphene.Boolean()
    current_page_number = graphene.Int()
    next_page_number = graphene.Int()
    previous_page_number = graphene.Int()
    number_of_pages = graphene.Int()
    total_elements = graphene.Int()
    pages_number_array = graphene.List(graphene.Int)

    @classmethod
    def get_page(self, page_datas, page_number, total_items):
        page_object = page_datas.page(page_number)
        previous_page_number = 0
        next_page_number = 0

        if page_object.number > 1:
            previous_page_number = page_object.previous_page_number()
        try:
            next_page_number = page_object.next_page_number()
        except:
            next_page_number + page_object.number

        return self(
            number=page_object.number,
            has_next_page=page_object.has_next(),
            has_previous_page=page_object.has_previous(),
            current_page_number = page_number,
            next_page_number=next_page_number,
            previous_page_number=previous_page_number,
            number_of_pages = page_datas.num_pages,
            total_elements = total_items,
            pages_number_array = list(range(1, page_datas.num_pages + 1))
        ), page_object