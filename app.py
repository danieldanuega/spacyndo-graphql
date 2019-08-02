from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, Field, Schema, String, List
import spacy

app = Flask(__name__)
nlp = spacy.load('id_ud-tag-dep-ner-1.0.0')


# Model --> that represent the structure of the Spacy model and handle the function
class Model(ObjectType):
    text = String()
    token = List(String)
    pos = List(String)
    dep = List(String)
    ner = List(String)

    def resolve_token(parent, info):
        doc = nlp(parent.text)
        result = []
        for token in doc:
            result.append(token.text)
        return result

    def resolve_pos(parent, info):
        doc = nlp(parent.text)
        result = []
        for token in doc:
            result.append((token.text,token.pos_))
        return result

    def resolve_dep(parent, info):
        doc = nlp(parent.text)
        result = []
        for token in doc:
            result.append((token.text, token.dep_))
        return result

    def resolve_ner(parent, info):
        doc = nlp(parent.text)
        result = []
        for ent in doc.ents:
            result.append((ent.text, ent.label_))
        return result


# Schema --> this is the endpoint source of truth
class Query(ObjectType):
    do_prediction = Field(Model, text=String(required=True))

    def resolve_do_prediction(parent, info, text):
        return Model(text=text)

schema = Schema(query=Query)


# Route --> expose it!
@app.route('/')
def index():
    return '<h1> Greetings! welcome to Spacy ID GraphQL, please append /graphql to open Graphiql</h1>'

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__ == '__main__':
    app.run()
