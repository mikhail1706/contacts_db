
        var vue =new Vue({
            el: '#app',
            vuetify: new Vuetify(),
            data: {
                show1: false,
                show2: false,
                password: '',
                password2: '',
                rules: {
                    required: value => !!value || 'Required.',
                    min: v => v.length >= 8 || 'Min 8 characters',
                    checkSamePasswords: val => val === document.getElementById('id_password1').value || 'Passwords are difference',
                },
                nameRules: [
                    v => !!v || 'Name is required',
                    v => (v && v.length <= 10) || 'Name must be less than 10 characters',
                ],
                emailRules: [
                    v => !!v || 'E-mail is required',
                    v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
                ]
            },
            methods: {
                validate() {
                    this.$refs.form.validate()
                },
            }
        })
