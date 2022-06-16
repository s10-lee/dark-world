import { SET_PAGE_LOADER } from 'store/types'
import { getApiCall, postApiCall, putApiCall, deleteApiCall } from 'services/http'

export const apiCrudMixin = {
    props: {
        pk: {
            type: [String, Number],
            default: null,
        }
    },
    data() {
        return {
            title: null,
            pkName: 'id',
            item: null,
            items: null,
            endpoint: null,
            errors: [],
            fields: [],
            notifyDuration: 5000,
        }
    },
    computed: {
        routePath() {
            return (this.pk
                ? this.$route.fullPath.replace(this.pk.toString(), '')
                : this.$route.path).replace(/\/$/, '')
        }
    },
    methods: {
        loading(status) {
            this.$store.commit(SET_PAGE_LOADER, status)
        },
        notify(message, type = null, duration = null) {
            this.$store.dispatch('notify', {
                message: message,
                type: type || 'success',
                duration: duration || this.notifyDuration,
            })
        },
        makePayload() {
            if (this.item) {
                const payload = {}
                this.fields.map(item => {
                    if (item.field !== this.pkName) {
                        payload[item.field] = this.item[item.field]
                    }
                })
                return payload
            }
            return null
        },
        createEmptyItem() {
            this.item = {}
            this.fields.map(item => {
                if (item.field !== this.pkName) {
                    this.item[item.field] = null
                }
            })
        },
        endpointUrl(pk = null) {
            const url = `${this.endpoint}/${pk ? pk : ''}/`
            return url.replaceAll(/\/+/g, '/')
        },
        listItems() {
            return getApiCall(this.endpointUrl())
                .then(data => this.items = data)
                .catch(error => this.errors.push(error))
        },
        receiveItem(pk) {
            return getApiCall(this.endpointUrl(pk))
                .then(data => this.item = data)
                .catch(error => this.errors.push(error))

        },
        createItem(payloadData) {
            return postApiCall(this.endpointUrl(), payloadData)
                .then(data => this.item = data)
                .catch(error => this.errors.push(error))
                .then(() => {
                    this.notify('Item was created !')
                    this.$router.push(this.routePath + '/' + this.item[this.pkName])
                })
        },
        updateItem(pk, payloadData) {
            this.loading(true)
            return putApiCall(this.endpointUrl(pk), payloadData)
                .then(data => this.item = data)
                .catch(error => this.errors.push(error))
                .then(() => {
                    // this.$router.go(0)
                    this.notify('Item was updated !')
                    setTimeout(() => this.loading(false), 300)
                })
        },
        destroyItem(pk) {
            if (confirm('Delete this item ?')) {
                return deleteApiCall(this.endpointUrl(pk))
                    .catch(error => this.errors.push(error))
                    .then(() => {
                        this.notify('Item was deleted !')
                        this.$router.push(this.routePath)
                    })
            }
        },
        saveFormItem() {
            const payload = this.makePayload()
            // console.log('saveFormItem -> payload', payload)
            this.pk === 'add' ? this.createItem(payload) : this.updateItem(this.pk, payload)

        },
    },
    mounted() {
        if (this.pk === 'add') {
            this.createEmptyItem()
        } else if (this.pk) {
            this.receiveItem(this.pk)
        }
        this.listItems()
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