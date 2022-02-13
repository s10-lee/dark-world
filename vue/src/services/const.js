export const BASE_API_URL = '/api'
export const API_OBTAIN_URL = BASE_API_URL + '/token/obtain/'
export const API_REFRESH_URL = BASE_API_URL + '/token/refresh/'

export const ROUTE_AUTH = { meta: { authRequired: true }, props: true}
export const ROUTE_GUEST = { meta: { onlyGuest: true }, props: true}

export const HTTP_METHODS = {
    'GET': 'GET',
    'POST': 'POST',
    'PUT': 'PUT',
    'PATCH': 'PATCH',
    'DELETE': 'DELETE',
}