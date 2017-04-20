import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from .models import NucleicAcidType, Sample
from library_sample_shared.models import (Organism, ConcentrationMethod,
                                          ReadLength, LibraryProtocol,
                                          LibraryType)
User = get_user_model()


# Models

class NucleicAcidTypeTest(TestCase):
    def setUp(self):
        self.nucleic_acid_type = NucleicAcidType(name='NAT')

    def test_nucleic_acid_type_name(self):
        self.assertTrue(isinstance(self.nucleic_acid_type, NucleicAcidType))
        self.assertEqual(
            self.nucleic_acid_type.__str__(),
            self.nucleic_acid_type.name,
        )


# Views

class GetNucleicAcidTypesTest(TestCase):
    def setUp(self):
        User.objects.create_user(email='foo@bar.io', password='foo-foo')

    def test_nucleic_acid_types(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.get(reverse('get_nucleic_acid_types'))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.content), b'[]')


class SaveSampleTest(TestCase):
    def setUp(self):
        User.objects.create_user(email='foo@bar.io', password='foo-foo')

        self.library_protocol = LibraryProtocol(
            name='Protocol',
            provider='',
            catalog='',
            explanation='',
            input_requirements='',
            typical_application='',
        )
        self.library_protocol.save()

        self.library_type = LibraryType(name='Library Type')
        self.library_type.save()
        self.library_type.library_protocol.add(self.library_protocol)

        self.nucleic_acid_type = NucleicAcidType(name='NAT')
        self.nucleic_acid_type.save()

        self.organism = Organism(name='Human')
        self.organism.save()

        self.method = ConcentrationMethod(name='fluorography')
        self.method.save()

        self.read_length = ReadLength(name='1x50')
        self.read_length.save()

        self.test_sample = Sample(
            name='Sample_edit',
            organism_id=self.organism.pk,
            concentration=1.0,
            concentration_method_id=self.method.pk,
            read_length_id=self.read_length.pk,
            sequencing_depth=1,
            nucleic_acid_type_id=self.nucleic_acid_type.pk,
            library_protocol_id=self.library_protocol.pk,
            library_type_id=self.library_type.pk,
        )
        self.test_sample.save()

    def test_save_ok(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.post(reverse('save_sample'), {
            'mode': 'add',
            'records': json.dumps([{
                'name': 'Sample_add',
                'organism': self.organism.pk,
                'concentration': 1.0,
                'concentration_method': self.method.pk,
                'read_length': self.read_length.pk,
                'sequencing_depth': 1,
                'nucleic_acid_type': self.nucleic_acid_type.pk,
                'library_protocol': self.library_protocol.pk,
                'library_type': self.library_type.pk,
            }])
        })
        self.assertEqual(response.status_code, 200)
        sample = Sample.objects.get(name='Sample_add')
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': True,
            'error': [],
            'data': [{
                'name': sample.name,
                'recordType': 'S',
                'sampleId': sample.pk,
                'barcode': sample.barcode,
            }],
        })

    def test_wrong_http_method(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.get(reverse('save_sample'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': False,
            'error': 'Could not save the sample(s).',
            'data': [],
        })

    def test_missing_records(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.post(reverse('save_sample'), {'mode': 'add'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': False,
            'error': 'Could not save the sample(s).',
            'data': [],
        })

    def test_wrong_or_missing_mode(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.post(reverse('save_sample'), {
            'records': '[{}]'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': False,
            'error': 'Could not save the sample(s).',
            'data': [],
        })

    def test_not_unique_name(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.post(reverse('save_sample'), {
            'mode': 'add',  # works for 'edit' too
            'records': json.dumps([{
                'name': 'Sample_edit',
            }])
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': False,
            'error': [{
                'name': 'Sample_edit',
                'value': 'Sample with this Name already exists.'
            }],
            'data': [],
        })

    def test_missing_or_invalid_fields(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.post(reverse('save_sample'), {
            'mode': 'add',  # works for 'edit' too
            'records': json.dumps([{
                'name': 'Sample',
            }])
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': False,
            'error': [{
                'name': 'Sample',
                'value': 'Could not save the sample.'
            }],
            'data': [],
        })

    def test_edit_ok(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.post(reverse('save_sample'), {
            'mode': 'edit',
            'records': json.dumps([{
                'sample_id': self.test_sample.pk,
                'name': 'Sample_edit_new',
                'organism': self.organism.pk,
                'equal_representation_nucleotides': 'true',
                'concentration': 1.0,
                'concentration_method': self.method.pk,
                'read_length': self.read_length.pk,
                'sequencing_depth': 1,
                'nucleic_acid_type': self.nucleic_acid_type.pk,
                'library_protocol': self.library_protocol.pk,
                'library_type': self.library_type.pk,
                'comments': '',
            }]),
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': True,
            'error': [],
            'data': [],
        })

    def test_missing_or_empty_sample_id(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.post(reverse('save_sample'), {
            'mode': 'edit',
            'records': json.dumps([{
                'name': 'Sample'
            }])
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': False,
            'error': 'Could not save the sample(s).',
            'data': [],
        })


class DeleteSampleTest(TestCase):
    def setUp(self):
        User.objects.create_user(email='foo@bar.io', password='foo-foo')
        self.sample = Sample.get_test_sample('Sample')
        self.sample.save()

    def test_delete_sample(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.post(reverse('delete_sample'), {
            'record_id': self.sample.pk
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': True, 'error': '',
        })

    def test_wrong_http_method(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.get(reverse('delete_sample'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': False, 'error': 'Could not delete the sample.',
        })

    def test_missing_or_empty_record_id(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.post(reverse('delete_sample'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': False, 'error': 'Could not delete the sample.',
        })

    def test_non_existing_record_id(self):
        self.client.login(email='foo@bar.io', password='foo-foo')
        response = self.client.post(reverse('delete_sample'), {
            'record_id': '-1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, 'utf-8'), {
            'success': False, 'error': 'Could not delete the sample.',
        })
