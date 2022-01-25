import { getApiCall, postApiCall, putApiCall, deleteApiCall } from 'services/http'

export const apiCrudMixin = {
    props: ['pk'],
    data() {
        return {
            item: null,
            items: null,
            endpoint: null,
            errors: [],
        }
    },
    methods: {
        endpointUrl(pk = null) {
            return `${this.endpoint}/${pk ? pk : ''}/`.replace('//', '/')
        },
        listItems() {
            getApiCall(this.endpointUrl())
                .then(data => this.items = data)
                .catch(error => this.errors.push(error))
        },
        receiveItem(pk) {
            getApiCall(this.endpointUrl(pk))
                .then(data => this.item = data)
                .catch(error => this.errors.push(error))

        },
        createItem(payloadData) {
            postApiCall(this.endpointUrl(), payloadData)
                .then(data => this.item = data)
                .catch(error => this.errors.push(error))
        },
        updateItem(pk, payloadData) {
            putApiCall(this.endpointUrl(pk), payloadData)
                .then(data => this.item = data)
                .catch(error => this.errors.push(error))
        },
        destroyItem(pk) {
            deleteApiCall(this.endpointUrl(pk))
                .then(() => {
                    this.item = null
                    this.pk = null
                })
                .catch(error => this.errors.push(error))
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
        }
        this.listItems()
    }
}
