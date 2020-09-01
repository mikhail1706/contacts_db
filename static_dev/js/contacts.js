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
            first_name: '',
            last_name: '',
            city: '',
            country: '',
            phone_number: '',
            email: '',
            date_of_birth: new Date().toISOString().substr(0, 10),
        },
        defaultItem: {
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
    computed: {
        formTitle() {
            return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
        },
    },
    methods: {
        editItem(item) {
            this.editedIndex = this.contacts.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
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
                Object.assign(this.contacts[this.editedIndex], this.editedItem)
            } else {
                axios.post('/contacts/create/', this.editedItem)
                    .then(response => {
                        if (response.data.success) {
                            this.contacts.push(
                                response.data.data.new_contact
                            )
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
            this.close()
        },
        customFilter(slot) {
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
        getAllData() {
            axios
                .all([
                    axios.get('/contacts/all/'),
                ])
                .then(axios.spread((contacts,) => {
                        this.contacts = contacts.data.data.contacts;
                        this.headers = contacts.data.data.headers;

                        this.cities = contacts.data.data.cities;
                        this.countries = contacts.data.data.countries;
                    }
                ))
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
