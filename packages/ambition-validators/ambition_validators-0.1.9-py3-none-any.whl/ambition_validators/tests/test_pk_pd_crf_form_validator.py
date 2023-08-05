from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES

from ..form_validators import PkPdCrfFormValidator


class TestPkPdCrfFormValidator(TestCase):

    def test_flucytosine_dose_one_given_yes(self):
        cleaned_data = {'flucytosine_dose_one_given': YES,
                        'flucytosine_dose_one_datetime': None}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('flucytosine_dose_one_datetime', form_validator._errors)

    def test_flucytosine_dose_one_given_no(self):
        cleaned_data = {'flucytosine_dose_one_given': NO,
                        'flucytosine_dose_one_datetime': get_utcnow()}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('flucytosine_dose_one_datetime', form_validator._errors)

    def test_flucytosine_dose_two_given_yes(self):
        cleaned_data = {'flucytosine_dose_two_given': YES,
                        'flucytosine_dose_two_datetime': None}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('flucytosine_dose_two_datetime', form_validator._errors)

    def test_flucytosine_dose_two_given_no(self):
        cleaned_data = {'flucytosine_dose_two_given': NO,
                        'flucytosine_dose_two_datetime': get_utcnow()}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('flucytosine_dose_two_datetime', form_validator._errors)

    def test_flucytosine_dose_three_given_yes(self):
        cleaned_data = {'flucytosine_dose_three_given': YES,
                        'flucytosine_dose_three_datetime': None}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            'flucytosine_dose_three_datetime', form_validator._errors)

    def test_flucytosine_dose_three_given_no(self):
        cleaned_data = {'flucytosine_dose_three_given': NO,
                        'flucytosine_dose_three_datetime': get_utcnow()}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            'flucytosine_dose_three_datetime', form_validator._errors)

    def test_flucytosine_dose_four_given_yes(self):
        cleaned_data = {'flucytosine_dose_four_given': YES,
                        'flucytosine_dose_four_datetime': None}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            'flucytosine_dose_four_datetime', form_validator._errors)

    def test_flucytosine_dose_four_given_no(self):
        cleaned_data = {'flucytosine_dose_four_given': NO,
                        'flucytosine_dose_four_datetime': get_utcnow()}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            'flucytosine_dose_four_datetime', form_validator._errors)

    def test_fluconazole_dose_given_yes(self):
        cleaned_data = {'fluconazole_dose_given': YES,
                        'fluconazole_dose_datetime': None}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            'fluconazole_dose_datetime', form_validator._errors)

    def test_fluconazole_dose_given_no(self):
        cleaned_data = {'fluconazole_dose_given': NO,
                        'fluconazole_dose_datetime': get_utcnow()}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            'fluconazole_dose_datetime', form_validator._errors)

    def test_fluconazole_dose_given_no_reason_missed_none(self):
        cleaned_data = {'fluconazole_dose_given': NO,
                        'fluconazole_dose_datetime': None,
                        'fluconazole_dose_reason_missed': None}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            'fluconazole_dose_reason_missed', form_validator._errors)

    def test_fluconazole_dose_given_no_reason_missed_not_none(self):
        cleaned_data = {'fluconazole_dose_given': YES,
                        'fluconazole_dose_datetime': get_utcnow(),
                        'fluconazole_dose_reason_missed': 'blah blah!!'}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            'fluconazole_dose_reason_missed', form_validator._errors)

    def test_full_ambisome_dose_given_yes(self):
        cleaned_data = {'ambisome_ended_datetime': None,
                        'full_ambisome_dose_given': YES, }
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('ambisome_ended_datetime', form_validator._errors)

    def test_full_ambisome_dose_given_no(self):
        cleaned_data = {'ambisome_ended_datetime': get_utcnow(),
                        'full_ambisome_dose_given': NO, }
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('ambisome_ended_datetime', form_validator._errors)

    def test_full_ambisome_dose_given_none(self):
        cleaned_data = {'ambisome_ended_datetime': get_utcnow(),
                        'full_ambisome_dose_given': None, }
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('ambisome_ended_datetime', form_validator._errors)

    def test_blood_sample_missed_no_reason_missed_none(self):
        cleaned_data = {'blood_sample_missed': YES,
                        'blood_sample_reason_missed': None}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            'blood_sample_reason_missed', form_validator._errors)

    def test_post_dose_lp(self):
        cleaned_data = {'pre_dose_lp': NO,
                        'post_dose_lp': None}
        form_validator = PkPdCrfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('post_dose_lp', form_validator._errors)
