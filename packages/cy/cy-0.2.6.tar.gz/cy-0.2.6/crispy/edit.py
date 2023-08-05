import re


class BaseEdit(object):
    PAM_WT_CAS9 = 'NGG'

    def __init__(self, edit_window=None, pam=None, base_edit=None, len_guide=None, name=None):
        self.edit_window = edit_window
        self.pam = pam
        self.base_edit = base_edit
        self.len_guide = len_guide
        self.name = name

    @staticmethod
    def base_complement(nucleotide):
        if nucleotide == 'C':
            return 'G'
        elif nucleotide == 'G':
            return 'C'
        elif nucleotide == 'A':
            return 'T'
        elif nucleotide == 'T':
            return 'A'

    @staticmethod
    def parse_coordinates(genomic_coordinates):
        chrm, pos = genomic_coordinates.split(':')
        chrm, start, end = chrm, int(pos.split('-')[0]), int(pos.split('-')[1])
        return chrm, start, end

    def assert_guide(self, guide):
        assert len(guide) == self.len_guide, f'Guide size: expected {self.len_guide} got {len(guide)}: {guide}'

        pam_regex = self.pam.replace('N', '.')
        assert re.search(f'{pam_regex}$', guide), f'PAM mismatch: expected {self.pam} got {guide[-len(self.pam):]}'

    def split_guide(self, guide):
        start = guide[:self.edit_window[0]]
        edit = guide[self.edit_window[0]:self.edit_window[1]]
        end = guide[self.edit_window[1]:-len(self.pam)]

        pam = guide[-len(self.pam):]

        return start, edit, end, pam

    def print_guide(self, guide):
        self.assert_guide(guide)

        start, edit, end, pam = self.split_guide(guide)

        print(f'{start} {edit} {end} [{pam}]')

    def edit_guide(self, guide, guide_strand, target_strand):
        start, edit, end, pam = self.split_guide(guide)

        if guide_strand == target_strand:
            edit = edit.replace(self.base_complement(self.base_edit[0]), self.base_complement(self.base_edit[1]))
        else:
            edit = edit.replace(self.base_edit[0], self.base_edit[1])

        return start + edit + end + pam

    def to_vep(self, guide_original, guide_edited):
        start_win, original, end_win, pam = self.split_guide(guide_original)
        _, edited, _, _ = self.split_guide(guide_edited)

        if original == edited:
            return None

        else:
            idx_start = min([i for i, bp in enumerate(original) if bp != edited[i]])
            idx_end = len(original) - min([i for i, bp in enumerate(original[::-1]) if bp != edited[::-1][i]])

            edit = f'{original[idx_start:idx_end]}/{edited[idx_start:idx_end]}'

            return edit, len(start_win) + idx_start, len(start_win) + (idx_end - 1)


class CytidineDeaminase(BaseEdit):
    def __init__(self, edit_window=(3, 8), pam=BaseEdit.PAM_WT_CAS9, len_guide=23, name='Cytidine deaminase'):
        super().__init__(
            edit_window=edit_window,
            pam=pam,
            base_edit=('C', 'T'),
            len_guide=len_guide,
            name=name
        )


class AdenineDeaminase(BaseEdit):
    def __init__(self, edit_window=(3, 8), pam=BaseEdit.PAM_WT_CAS9, len_guide=23, name='Adenine deaminase'):
        super().__init__(
            edit_window=edit_window,
            pam=pam,
            base_edit=('A', 'G'),
            len_guide=len_guide,
            name=name
        )
