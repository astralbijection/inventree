from haystack import indexes

from inventory.models import Item, Container


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    item_id = indexes.IntegerField(model_attr="id")

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ContainerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    container_id = indexes.IntegerField(model_attr="id")

    def get_model(self):
        return Container

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
