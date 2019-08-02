**Spacy ID GraphQL**

Welcome to the GraphQL for `https://github.com/danielgo13/dep-ner-spacy-id`.
This GraphQL use Flask framework and graphene for the library.

You can use this model to predict POS Tagging, Dependency Parser, and Named Entity Recognition.

**How To**

The url is: `spacy-id-ql.herokuapp.com/graphql`. Then a Graphiql will open.

```
{
    doPrediction(text: "your text here") {
        token
        pos
        dep
        ner
    }
}
```