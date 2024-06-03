import unittest
from main import app
from forms import LoginForm, RegisterForm, ReimbursementForm

class FormsTestCase(unittest.TestCase):

    # LOGIN FORM TESTS
    def test_login_form_valid(self):
        form = LoginForm(email='admin@example.com', password='password')
        self.assertTrue(form.validate())

    def test_login_form_invalid_email(self):
        form = LoginForm(email='invalid-email', password='password')
        self.assertFalse(form.validate())
        self.assertIn('Invalid email address.', form.email.errors)

    def test_login_form_empty_email(self):
        form = LoginForm(email='', password='password')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.email.errors)

    def test_login_form_empty_password(self):
        form = LoginForm(email='admin@example.com', password='')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.password.errors)



    # REGISTER FORM TESTS
    def test_register_form_valid(self):
        form = RegisterForm(first_name='John', last_name='Doe', email='john@nucleusteq.com', password='password789', confirm='password789', contact_no='1234567890', department='1', role='1')
        self.assertTrue(form.validate())

    def test_register_form_invalid_email(self):
        form = RegisterForm(first_name='John', last_name='Doe', email='invalid-email', password='password789', confirm='password789', contact_no='1234567890', department='1', role='1')
        self.assertFalse(form.validate())
        self.assertIn('Invalid email address.', form.email.errors)

    def test_register_form_password_mismatch(self):
        form = RegisterForm(first_name='John', last_name='Doe', email='john@nucleusteq.com', password='password', confirm='differentpassword', contact_no='1234567890', department='1', role='1')
        self.assertFalse(form.validate())
        self.assertIn('Field must be equal to confirm.', form.confirm.errors)

    def test_register_form_empty_first_name(self):
        form = RegisterForm(first_name='', last_name='Doe', email='john@nucleusteq.com', password='password', confirm='password', contact_no='1234567890', department='1', role='1')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.first_name.errors)

    def test_register_form_empty_last_name(self):
        form = RegisterForm(first_name='John', last_name='', email='john@nucleusteq.com', password='password', confirm='password', contact_no='1234567890', department='1', role='1')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.last_name.errors)

    def test_register_form_empty_contact_no(self):
        form = RegisterForm(first_name='John', last_name='Doe', email='john@nucleusteq.com', password='password', confirm='password', contact_no='', department='1', role='1')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.contact_no.errors)

    def test_register_form_invalid_contact_no(self):
        form = RegisterForm(first_name='John', last_name='Doe', email='john@nucleusteq.com', password='password', confirm='password', contact_no='91invalid-contact', department='1', role='1')
        self.assertFalse(form.validate())
        self.assertIn('Invalid phone number.', form.contact_no.errors)



    # REIMBURSEMENT FORM TESTS
    def test_reimbursement_form_valid(self):
        form = ReimbursementForm(email='employee@nucleusteq.com', amount=1000, expense_type='Travelling')
        self.assertTrue(form.validate())

    def test_reimbursement_form_invalid_email(self):
        form = ReimbursementForm(email='employee@example.com', amount=1000, expense_type='Travelling')
        self.assertFalse(form.validate())
        self.assertIn('Invalid email address.', form.email.errors)

    def test_reimbursement_form_empty_email(self):
        form = ReimbursementForm(email='', amount=1000, expense_type='Travelling')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.email.errors)

    def test_reimbursement_form_negative_amount(self):
        form = ReimbursementForm(email='employee@example.com', amount=-1000, expense_type='Travelling')
        self.assertFalse(form.validate())
        self.assertIn('Must be greater than or equal to 0.', form.amount.errors)

    def test_reimbursement_form_zero_amount(self):
        form = ReimbursementForm(email='employee@example.com', amount=0, expense_type='Travelling')
        self.assertFalse(form.validate())
        self.assertIn('Must be greater than 0.', form.amount.errors)

    def test_reimbursement_form_empty_expense_type(self):
        form = ReimbursementForm(email='employee@example.com', amount=1000, expense_type='')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.expense_type.errors)

    def test_reimbursement_form_invalid_expense_type(self):
        form = ReimbursementForm(email='employee@example.com', amount=1000, expense_type='InvalidType')
        self.assertFalse(form.validate())
        self.assertIn('Invalid expense type.', form.expense_type.errors)
