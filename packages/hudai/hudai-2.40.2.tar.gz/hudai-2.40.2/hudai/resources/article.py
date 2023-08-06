"""
hudai.resources.article
"""
from ..helpers.resource import Resource


class ArticleResource(Resource):
    def __init__(self, client):
        Resource.__init__(self, client, base_path='/articles')
        self.resource_name = 'Article'

    def list(self,
             article_type=None,
             importance_score_min=None,
             key_term=None,
             link_hash=None,
             person_id=None,
             published_after=None,
             published_before=None,
             page=None):
        return self._list(
            importance_score_min=importance_score_min,
            key_term=key_term,
            link_hash=link_hash,
            person_id=person_id,
            published_after=published_after,
            published_before=published_before,
            type=article_type,
            page=page
        )

    def create(self,
               article_type=None,
               authors=[],
               image_url=None,
               importance_score=None,
               link_url=None,
               published_at=None,
               raw_data_url=None,
               source_url=None,
               text=None,
               title=None):
        return self._create(
            authors=authors,
            image_url=image_url,
            importance_score=importance_score,
            link_url=link_url,
            published_at=published_at,
            raw_data_url=raw_data_url,
            source_url=source_url,
            text=text,
            title=title,
            type=article_type
        )

    def fetch(self, entity_id):
        return self._fetch(entity_id)

    def update(self, entity_id,
               article_type=None,
               authors=[],
               image_url=None,
               importance_score=None,
               link_url=None,
               published_at=None,
               raw_data_url=None,
               source_url=None,
               text=None,
               title=None):
        return self._update(
            entity_id,
            authors=authors,
            image_url=image_url,
            importance_score=importance_score,
            link_url=link_url,
            published_at=published_at,
            raw_data_url=raw_data_url,
            source_url=source_url,
            text=text,
            title=title,
            type=article_type
        )

    def delete(self, entity_id):
        return self._delete(entity_id)

    def key_terms(self, entity_id):
        return self.http_get('/{id}/key-terms',
                             params={'id': entity_id})

    def search(self,
               limit=None,
               offset=None,
               authors=None,
               company_id=None,
               created_after=None,
               created_before=None,
               key_terms=None,
               max_importance=None,
               min_importance=None,
               group_id=None,
               published_after=None,
               published_before=None,
               scored_after=None,
               scored_before=None,
               tags=None,
               text=None,
               type=None):
        return self.http_get(
            '/search',
            params={
                "limit": limit,
                "offset": offset,
                "authors": authors,
                "company_id": company_id,
                "created_after": created_after,
                "created_before": created_before,
                "key_terms": key_terms,
                "max_importance": max_importance,
                "min_importance": min_importance,
                "group_id": group_id,
                "published_after": published_after,
                "published_before": published_before,
                "scored_after": scored_after,
                "scored_before": scored_before,
                "tags": tags,
                "text": text,
                "type": type,
            })
