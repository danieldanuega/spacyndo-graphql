from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphene import ObjectType, Field, Schema, String, List, relay, ResolveInfo
import spacy

app = Flask(__name__)
CORS(app)
nlp = spacy.load('id_ud-tag-dep-ner-1.0.0')


# JSON Object
class Prediction(ObjectType):
    id = String()
    token = String()
    label = String()


# Model Object --> that represent the structure of the Spacy model and handle the function
class Model(ObjectType):
    class Meta:
        interfaces = (relay.Node, )

    text = String()
    token = List(Prediction)
    pos = List(Prediction)
    dep = List(Prediction)
    ner = List(Prediction)

    def resolve_token(parent, info: ResolveInfo):
        doc = nlp(parent.text)
        result = []
        predictions = []
        i=0
        for token in doc:
            predictions.append(('tok-'+str(i), token.text))
            i += 1
        for id, token in predictions:
            prediction = Prediction(id=id, token=token, label="-")
            result.append(prediction)

        return result

    def resolve_pos(parent, info: ResolveInfo):
        doc = nlp(parent.text)
        result = []
        predictions = []
        i=0
        for token in doc:
            predictions.append(('pos-'+str(i), token.text, token.pos_))
            i += 1
        for id, token, label in predictions:
            prediction = Prediction(id=id, token=token, label=label)
            result.append(prediction)

        return result

    def resolve_dep(parent, info: ResolveInfo):
        doc = nlp(parent.text)
        result = []
        predictions = []
        i = 0
        for token in doc:
            predictions.append(('dep-'+str(i), token.text, token.dep_))
            i += 1
        for id, token, label in predictions:
            prediction = Prediction(id=id, token=token, label=label)
            result.append(prediction)

        return result

    def resolve_ner(parent, info: ResolveInfo):
        doc = nlp(parent.text)
        result = []
        predictions = []
        i = 0
        for ent in doc.ents:
            predictions.append(('ner-'+str(i), ent.text, ent.label_))
            i += 1
        for id, token, label in predictions:
            prediction = Prediction(id=id, token=token, label=label)
            result.append(prediction)

        return result

    @classmethod
    def get_node(cls, info, id):
        return Model(id=id)


# Root Object, define your query here that actually consume by user later
class Query(ObjectType):
    do_prediction = Field(Model, text=String(required=True))
    node = relay.Node.Field()

    def resolve_do_prediction(parent, info, text):
        return Model(text=text)


# Schema --> this is the endpoint source of truth
schema = Schema(query=Query)


# Route --> expose it!
@app.route('/')
def index():
    return '<h1> Greetings! welcome to Spacy ID GraphQL, please append /graphql to open Graphiql</h1>'

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__ == '__main__':
    app.run()
