import json
from datetime import datetime, timedelta
from apps.commons.external_api_repository import OpenSearchService
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class UserLogService:
    @staticmethod
    def _build_query(must_clauses, page=1, limit=10):
        """
        Build a generic OpenSearch query with pagination and sorting.
        """
        offset = (page - 1) * limit
        return {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "must": must_clauses
                }
            },
            "sort": [
                {"timestamp": {"order": "desc"}},
                {"_id": {"order": "desc"}}
            ],
            "from": offset,
            "size": limit
        }

    @staticmethod
    def _execute_search(index_pattern, query):
        """
        Execute the search query using OpenSearchService.
        """
        opensearch_service = OpenSearchService()
        response = opensearch_service.search_by_index_and_query(index_pattern, json.dumps(query))
        if not response.get('result'):
            return None, _('Failed to fetch logs from OpenSearch')
        return response, None

    @staticmethod
    def _process_response(response, page, limit):
        """
        Process OpenSearch response and format it for the API.
        """
        if not response or 'hits' not in response:
            return None

        # Extract hits from the response
        hits = response['hits']['hits']
        total = response['hits']['total']['value']  # Total number of matching documents

        # Format results
        results = []
        for hit in hits:
            source = hit.get('_source', {})
            results.append({
                "url": source.get('url'),
                "method": source.get('method'),
                "action_type": source.get('action_type'),
                "status_code": source.get('status_code'),
                "status": source.get('status'),
                "timestamp": source.get('timestamp'),
                "company_id": source.get('company_id'),
                "username": source.get('username'),
                "metadata": source.get('metadata', {}),
                "object_type": source.get('object_type', 'unknown'),
                "created_at": source.get('created_at')
            })

        # Calculate pagination
        total_pages = max(1, (total + limit - 1) // limit)  # Ensure at least 1 page
        has_next = page < total_pages  # True if there are more pages
        has_previous = page > 1  # True if there is a previous page
        next_page = page + 1 if has_next else None  # Next page number or null
        previous_page = page - 1 if has_previous else None  # Previous page number or null

        return {
            "results": results,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,  # Total number of matching documents
                "total_pages": total_pages,  # Total number of pages
                "has_next": has_next,
                "has_previous": has_previous,
                "next_page": next_page,
                "previous_page": previous_page
            }
        }

    @staticmethod
    def get_logs_by_date(page=1, limit=10, start_date=None, end_date=None, company_id=None):
        """
        Get user logs from OpenSearch with pagination based on date range.
        """
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        must_clauses = [
            {
                "range": {
                    "created_at": {
                        "gte": f"{start_date.isoformat()}T00:00:00+07:00",
                        "lte": f"{end_date.isoformat()}T23:59:59+07:00"
                    }
                }
            }
        ]

        if company_id:
            must_clauses.append({
                "term": {
                    "company_id.keyword": company_id
                }
            })

        # Generate index patterns for all dates in range
        indices = []
        current_date = start_date
        while current_date <= end_date:
            index_name = f"user-log-result-meta-{current_date.strftime('%Y%m%d')}_{company_id}"
            indices.append(index_name)
            current_date += timedelta(days=1)

        query = {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "must": must_clauses
                }
            },
            "sort": [
                {"timestamp": {"order": "desc"}}
            ],
            "from": (page - 1) * limit,
            "size": limit
        }

        response, error = UserLogService._execute_search(indices, query)

        if error:
            return None, error
        return UserLogService._process_response(response, page, limit), None

    @staticmethod
    def filter_logs_by_username(username, page=1, limit=10, company_id=None):
        """
        Filter user logs by username from OpenSearch with pagination.
        """
        must_clauses = [
            {
                "term": {
                    "user_name.keyword": username
                }
            }
        ]

        if company_id:
            must_clauses.append({
                "term": {
                    "company_id.keyword": company_id
                }
            })

        # Search in both current and previous day's indices to ensure we find data
        current_date = datetime.now().date()
        prev_date = current_date - timedelta(days=1)
        indices = [
            f"user-log-result-meta-{current_date.strftime('%Y%m%d')}_{company_id}",
            f"user-log-result-meta-{prev_date.strftime('%Y%m%d')}_{company_id}"
        ]

        query = UserLogService._build_query(must_clauses, page, limit)
        response, error = UserLogService._execute_search(indices, query)

        if error:
            return None, error
        return UserLogService._process_response(response, page, limit), None

    @staticmethod
    def filter_logs(page, limit, start_time, end_time, username, action, status, company_id, object_type, metadata):
        try:
            # Convert datetime to OpenSearch format
            start_time_iso = start_time.isoformat()
            end_time_iso = end_time.isoformat()

            # Build base query with date range and company_id
            must_clauses = [
                {
                    "term": {
                        "company_id.keyword": company_id
                    }
                },
                {
                    "range": {
                        "created_at": {
                            "gte": start_time_iso,
                            "lte": end_time_iso
                        }
                    }
                }
            ]
            # Add optional filters
            if username:
                must_clauses.append({
                    "terms": {  # Use "terms" for list filtering
                        "username.keyword": username  # username is a list
                    }
                })
            if action:
                must_clauses.append({
                    "terms": {  # Use "terms" for list filtering
                        "action_type.keyword": action  # action is a list
                    }
                })
            if object_type:
                must_clauses.append({
                    "terms": {
                        "object_type.keyword": object_type
                    }
                })
            if status is not None:
                must_clauses.append({
                    "term": {
                        "status": status
                    }
                })
            if metadata:
                must_clauses.append({
                    "bool": {
                        "should": [
                            # Search within the raw JSON representation
                            {
                                "query_string": {
                                    "fields": ["metadata", "metadata.*"],
                                    "query": f"{metadata}",
                                    "analyze_wildcard": True
                                }
                            },
                            # Search for specific values in case it's stored as a JSON string
                            {
                                "wildcard": {
                                    "metadata.keyword": {
                                        "value": f"{metadata}",
                                        "case_insensitive": True
                                    }
                                }
                            },
                            # Search for metadata.name if mapped
                            {
                                "wildcard": {
                                    "metadata.name": {
                                        "value": f"{metadata}",
                                        "case_insensitive": True
                                    }
                                }
                            },
                            # Search for metadata.serial if mapped
                            {
                                "wildcard": {
                                    "metadata.serial": {
                                        "value": f"{metadata}",
                                        "case_insensitive": True
                                    }
                                }
                            }
                        ]
                    }
                })

            # Generate index patterns for the date range
            indices = []
            current_date = start_time.date()
            end_date = end_time.date()

            while current_date <= end_date:
                index_name = f"user-log-result-meta-{current_date.strftime('%Y%m%d')}"
                indices.append(index_name)
                current_date += timedelta(days=1)

            # Build and execute the query
            query = {
                "track_total_hits": True,
                "query": {
                    "bool": {
                        "must": must_clauses
                    }
                },
                "sort": [
                    {"timestamp": {"order": "desc"}}
                ],
                "from": (page - 1) * limit,
                "size": limit
            }
            response, error = UserLogService._execute_search(indices, query)

            if error:
                return None, error

            # Process and return the results
            return UserLogService._process_response(response, page, limit), None

        except Exception as e:
            logger.error(f"Error filtering logs: {str(e)}")
            return None, str(e)

    @staticmethod
    def filter_by_metadata_value(company_id: str, metadata_value: str, page: int = 1, limit: int = 10):
        """
        Filter logs by metadata value with pagination
        Args:
            company_id: Company ID to filter
            metadata_value: Value to search in metadata field
            page: Page number (1-based)
            limit: Number of items per page
        Returns:
            Tuple of (results, error) where results contains the paginated data
        """
        try:
            # Build the base query
            must_clauses = [
                {
                    "term": {
                        "company_id.keyword": company_id
                    }
                }
            ]

            # Add metadata value filter if provided
            if metadata_value:
                must_clauses.append({
                    "bool": {
                        "should": [
                            {
                                "wildcard": {
                                    "metadata.serial": {
                                        "value": f"*{metadata_value}*",
                                        "case_insensitive": True
                                    }
                                }
                            },
                            {
                                "query_string": {
                                    "query": f"metadata:*{metadata_value}*",
                                    "analyze_wildcard": True
                                }
                            }
                        ]
                    }
                })

            # Calculate pagination parameters
            from_ = (page - 1) * limit

            # Build the complete query
            query = {
                "query": {
                    "bool": {
                        "must": must_clauses
                    }
                },
                "sort": [
                    {"timestamp": {"order": "desc"}}
                ],
                "from": from_,
                "size": limit
            }

            # Get the index pattern
            index_pattern = f"user-log-result-meta-*_{company_id}"

            logger.debug(f"Executing query: {json.dumps(query)}")

            # Execute the search
            opensearch_service = OpenSearchService()
            response = opensearch_service.search_by_index_and_query(
                indices=index_pattern,
                query=json.dumps(query)
            )

            # Handle the response safely
            if not response or not isinstance(response, dict):
                return None, "Invalid response from OpenSearch"

            # Check if we have hits
            hits = response.get('hits', {}).get('hits', [])
            total_hits = response.get('hits', {}).get('total', {}).get('value', 0)
            total_pages = (total_hits + limit - 1) // limit

            # Format the results
            results = {
                "results": [hit.get('_source') for hit in hits],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_hits,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_previous": page > 1,
                    "next_page": page + 1 if page < total_pages else None,
                    "previous_page": page - 1 if page > 1 else None
                }
            }

            return results, None

        except Exception as e:
            logger.error(f"Error filtering logs by metadata value: {str(e)}")
            return None, str(e)

    @staticmethod
    def get_usernames_by_company_id(company_id, size=1000):
        """
        Retrieve usernames from OpenSearch for a specific company_id.

        Args:
            company_id (str): The company ID to query.
            size (int): Maximum number of usernames to return (default: 1000).

        Returns:
            list: List of usernames for the given company_id.
        """
        try:
            # Construct the index name for the company
            index_name = f"{settings.USER_LOG_USERNAME_INDEX_FORMAT}_{company_id}"

            # Define the query to fetch all usernames
            query = {
                "size": size,
                "query": {
                    "match_all": {}
                },
                "_source": ["username"]  # Only retrieve the username field
            }

            # Execute the search query
            response = UserLogService._execute_search(index_name, query)

            # Extract usernames from the response
            if response and 'hits' in response and 'hits' in response['hits']:
                usernames = []
                for hit in response['hits']['hits']:
                    if '_source' in hit and 'username' in hit['_source']:
                        usernames.append(hit['_source']['username'])
                return usernames
            else:
                logger.warning(f"No usernames found for company_id: {company_id}")
                return []

        except Exception as e:
            logger.error(f"Error retrieving usernames for company_id {company_id}: {str(e)}")
            return []
