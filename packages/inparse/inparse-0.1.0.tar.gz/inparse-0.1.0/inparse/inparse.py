import requests
from bs4 import BeautifulSoup
import lxml.html
import lxml.html.clean
import json
import pprint
from dateutil.parser import parse as date_parser

class InparseException(Exception):
     pass
class Inparse(object):

    TEST_MODE=False
    REPO_URI='http://inparse.com/api/parser?parser_no={}&access_token={}'
    TEST_REPO_URI = 'http://0.0.0.0:8080/api/parser?parser_no={}&access_token={}'
    def __init__(self,parser_no,access_token,parser_json=None):

        if parser_json:
            self.parser_json = json.loads(parser_json)
        else:
            self.parser_no=parser_no
            self.access_token=access_token
            if self.TEST_MODE:
                url=self.TEST_REPO_URI.format(parser_no,access_token)
            else:
                url = self.REPO_URI.format(parser_no, access_token)
            res=requests.get(url)
            self.parser_json=res.json()

        self.downloader=requests
        self.rules=self.bulid_rule_dict(self.parser_json['selectors'])



    def bulid_rule_dict(self,rl):
        rule_dict={}
        for r in rl:
            rule_dict[r['sid']]=r


        return rule_dict

    def parse_url(self,url):
        if url is None :
            raise InparseException('empty input')
        html = self.downloader.get(url).text
        return self.parse(html)

    def parse(self,html):
        if html is None :
            raise InparseException('empty input')




        dom=BeautifulSoup(html,'lxml')
        parent_sid=[]
        for id,r in self.rules.items():
            if r['parent_sid']:
                parent_sid.append(r['parent_sid'])

        parent_nodes={}
        for id in parent_sid:
            rule=self.rules[id]
            parent_nodes[id]=dom.select(rule['selector'])

        result_nodes = {}
        for id, rule in self.rules.items():
            if id in parent_sid:
                continue


            result_nodes[rule['name']]=[]
            result=result_nodes[rule['name']]

            if rule['parent_sid']:
                for node in parent_nodes[rule['parent_sid']]:
                    result.extend(node.select(rule['selector']))

            else:

                result.extend(dom.select(rule['selector']))


        return self.post_clean(result_nodes)


    @classmethod
    def article_clean(cls,nodes):

        ## will keep tgas
        content=''
        for n in nodes:
            content+=str(n)

        article_cleaner = lxml.html.clean.Cleaner()
        article_cleaner.javascript = True
        article_cleaner.style = True
        article_cleaner.safe_attrs_only=True
        article_cleaner.safe_attrs=['href','src','alt','height','width']
        article_cleaner.inline_style=True
        article_cleaner.allow_tags = [
            'a', 'span', 'p', 'br', 'strong', 'b',
            'em', 'i', 'tt', 'code', 'pre', 'blockquote', 'img', 'h1',
            'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'dl', 'dt', 'dd']
        article_cleaner.remove_unknown_tags = False
        return article_cleaner.clean_html(content)





    @classmethod
    def image_clean(cls,nodes):
        src=set()
        for n in nodes:
            if n.name == 'img' and 'src' in n.attrs:
                src.add(n.attrs['src'])
            else:
                for cn in n.find_all('img'):
                    if cn.name == 'img' and 'src' in n.attrs:
                        src.add(n.attrs['src'])


        return list(src)

    @classmethod
    def date_clean(cls,nodes):
        text=''
        for n in nodes:
            text=n.text.strip()

            try:
                for s in text.split(' '):
                    print(s)
                    return date_parser(s)
            except:
                pass
        return None

    @classmethod
    def text_clean(cls,nodes):
        text=''
        for n in nodes:
            text+=n.text
        return text.strip(' ')

    @classmethod
    def post_clean(cls,result_nodes):

        result={}
        for name,nodes in result_nodes.items():
            if 'article' in name:
                result[name]=cls.article_clean(nodes)

            elif 'image' in name:

                result[name] = cls.image_clean(nodes)

            elif  'date' in name:

                result[name] = cls.date_clean(nodes)

            else:

                result[name] = cls.text_clean(nodes)


        return result

    @classmethod
    def pretty_print(cls,d):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(d)
