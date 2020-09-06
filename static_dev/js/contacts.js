var vm = new Vue({
    el: '#contacts',
    vuetify: new Vuetify(),
    delimiters: ["{[", "]}"],
    data: {
        date: new Date().toISOString().substr(0, 10),
        menu: false,
        modal: false,
        dialog: false,
        editedIndex: -1,
        editedItem: {
            id: '',
            first_name: '',
            last_name: '',
            city: '',
            country: '',
            phone_number: '',
            email: '',
            date_of_birth: new Date().toISOString().substr(0, 10),
        },
        defaultItem: {
            id: '',
            first_name: '',
            last_name: '',
            city: '',
            country: '',
            phone_number: '',
            email: '',
            date_of_birth: new Date().toISOString().substr(0, 10),
        },
        citySearch: undefined,
        countrySearch: undefined,
        contacts: [],
        headers: [],
        cities: [],
        countries: [],
        rules: {
            required: value => !!value || 'Required.',
        },
        nameRules: [
            v => !!v || 'Name is required',
        ],
        emailRules: [
            v => !!v || 'E-mail is required',
            v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
        ]
    },
    methods: {
        editItem(item) {
            this.editedIndex = this.contacts.indexOf(item)
            this.dialog = true
            this.editedItem = Object.assign({}, item)
        },
        confirmDeleting(){

        },
        deleteItem(item) {
            const index = this.contacts.indexOf(item)
            confirm('Are you sure you want to delete this item?') && this.contacts.splice(index, 1)
        },
        close() {
            this.dialog = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },
        save() {
            if (this.editedIndex > -1) {
                axios.post(`/contacts/update/${this.editedItem.id}/`, this.editedItem)
                    .then(response => {
                        if (response.data.success) {
                            let contactIndex = this.contacts.findIndex(contact => contact.id === this.editedItem.id)
                            Object.assign(this.contacts[contactIndex], this.editedItem)
                            this.close()

                            iziToast.success({
                                timeout: 3000,
                                position: 'topLeft',
                                message: response.data.msg,
                            });
                        } else {
                            iziToast.error({
                                timeout: 3000,
                                title: 'Error',
                                message: response.data.msg,
                            });
                        }
                    })

            } else {
                axios.post('/contacts/create/', this.editedItem)
                    .then(response => {
                        if (response.data.success) {
                            this.contacts.push(
                                response.data.data.new_contact
                            )
                            this.close()
                            iziToast.success({
                                timeout: 3000,
                                position: 'topLeft', // bottomRight, bottomLeft, topRight, topLeft,
                                message: response.data.msg,
                            });
                        } else {
                            iziToast.error({
                                timeout: 3000,
                                position: 'topLeft',
                                title: 'Error',
                                message: response.data.msg,
                            });
                        }
                    })
            }

        },
        getAllData() {
            axios.all([
                axios.get('/contacts/all/'),
            ]).then(axios.spread((contacts,) => {
                    this.contacts = contacts.data.data.contacts;
                    this.headers = contacts.data.data.headers;

                    this.cities = contacts.data.data.cities;
                    this.countries = contacts.data.data.countries;
                }
            ))
        },
    },
    computed: {
        filteredContacts() {
            let filteredContacts = this.contacts
            if (this.citySearch) {
                filteredContacts = this.contacts
                    .filter(contact => {
                        return contact.city.includes(this.citySearch)
                    })
            }
            if (this.countrySearch) {
                filteredContacts = filteredContacts
                    .filter(contact => {
                        return contact.country.includes(this.countrySearch)
                    })
            }
            return filteredContacts
        },
        formTitle() {
            return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
        },
    },
    watch: {
        dialog(val) {
            val || this.close()
        },
    },
    created: function () {
    },
    mounted: function () {
        this.getAllData();
    }
});
