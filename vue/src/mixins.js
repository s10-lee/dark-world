import { SET_PAGE_LOADER } from 'store/types'
import { getApiCall, postApiCall, putApiCall, deleteApiCall } from 'services/http'

export const apiCrudMixin = {
    props: ['pk'],
    data() {
        return {
            item: null,
            items: null,
            endpoint: null,
            routePath: '',
            errors: [],
            fields: {},
            listFields: {},
            loaded: false,
        }
    },
    methods: {
        makePayload() {
            if (this.item) {
                let payload = {}
                Object.keys(this.fields).map(fieldName => {
                    payload[fieldName] = this.item[fieldName]
                })
                return payload
            }
            return null
        },
        createEmptyItem() {
            this.item = this.getEmptyFields()
        },
        getEmptyFields() {
            return {...this.fields}
        },
        endpointUrl(pk = null) {
            return `${this.endpoint}/${pk ? pk : ''}/`.replace('//', '/')
        },
        listItems() {
            this.loaded = false
            return getApiCall(this.endpointUrl())
                .then(data => this.items = data)
                .catch(error => this.errors.push(error))
                .then(() => this.loaded = true)
        },
        receiveItem(pk) {
            this.loaded = false
            return getApiCall(this.endpointUrl(pk))
                .then(data => this.item = data)
                .catch(error => this.errors.push(error))
                .then(() => this.loaded = true)

        },
        createItem(payloadData) {
            this.loaded = false
            return postApiCall(this.endpointUrl(), payloadData)
                .then(data => this.item = data)
                .catch(error => this.errors.push(error))
                .then(() => this.loaded = true)
        },
        updateItem(pk, payloadData) {
            this.loaded = false
            return putApiCall(this.endpointUrl(pk), payloadData)
                .then(data => this.item = data)
                .catch(error => this.errors.push(error))
                .then(() => this.loaded = true)
        },
        destroyItem(pk) {
            this.loaded = false
            return deleteApiCall(this.endpointUrl(pk))
                .then(() => {
                    this.item = null
                })
                .catch(error => this.errors.push(error))
                .then(() => this.loaded = true)
        },
        saveItem(payloadData, pk = null) {
            if (pk) {
                return this.updateItem(pk, payloadData)
            }
            return this.createItem(payloadData)
        },
    },
    mounted() {
        if (this.pk) {
            this.receiveItem(this.pk)
        } else {
            this.listItems()
        }
    }
}

export const PageMixin = {
    methods: {
        loading(status) {
            this.$store.commit(SET_PAGE_LOADER, status)
        },
        notify(message, type = null, duration = null) {
            this.$store.dispatch('notify', {
                message: message,
                type: type,
                duration: duration || 5000,
            })
        }
    }
}

export const ComponentMixin = {
    data() {
        return {
            sizes: ['xl', 'lg', 'md', 'sm', 'xs']
        }
    },
}