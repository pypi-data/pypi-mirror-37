from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator


class PkPdCrfFormValidator(FormValidator):

    def clean(self):

        for num in ['one', 'two', 'three', 'four']:
            self.required_if(
                YES,
                field=f'flucytosine_dose_{num}_given',
                field_required=f'flucytosine_dose_{num}_datetime')
            self.required_if(
                YES,
                field=f'flucytosine_dose_{num}_given',
                field_required=f'flucytosine_dose_{num}')
            self.required_if(
                NO,
                field=f'flucytosine_dose_{num}_given',
                field_required=f'flucytosine_dose_reason_missed',
                inverse=False)

        self.required_if(
            YES,
            field='fluconazole_dose_given',
            field_required='fluconazole_dose_datetime')

        self.required_if(
            NO,
            field='fluconazole_dose_given',
            field_required='fluconazole_dose_reason_missed')

        self.required_if(
            YES,
            field='full_ambisome_dose_given',
            field_required='ambisome_ended_datetime')

        self.required_if(
            YES,
            field='blood_sample_missed',
            field_required='blood_sample_reason_missed',
            inverse=False)

        self.required_if(
            NO,
            field='pre_dose_lp',
            field_required='post_dose_lp')
