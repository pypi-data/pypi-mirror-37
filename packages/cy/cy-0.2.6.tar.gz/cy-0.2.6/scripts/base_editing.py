import ast
import pandas as pd
from crispy.edit import CytidineDeaminase, AdenineDeaminase


def filter_offtarget(glib, max_offtarget=1):
    return glib[[ast.literal_eval(goff)[0] == max_offtarget for goff in glib['off_target_summary']]]


if __name__ == '__main__':
    ppdir = '/Users/eg14/Data/resources/phosphositeplus/'

    reg_phospho = pd.read_csv(f'{ppdir}/Phosphorylation_site_dataset.txt', sep='\t', skiprows=3)\
        .query("ORGANISM == 'human'")

    reg_acetyl = pd.read_csv(f'{ppdir}/Acetylation_site_dataset.txt', sep='\t', skiprows=3)\
        .query("ORGANISM == 'human'")

    reg_methy = pd.read_csv(f'{ppdir}/Methylation_site_dataset.txt', sep='\t', skiprows=3)\
        .query("ORGANISM == 'human'")

    reg_sumoy = pd.read_csv(f'{ppdir}/Sumoylation_site_dataset.txt', sep='\t', skiprows=3)\
        .query("ORGANISM == 'human'")

    # -
    dfile = '/Users/eg14/Downloads/WGE_JAK1_guides.tsv'

    glib = pd.read_csv(dfile, sep='\t')
    glib = filter_offtarget(glib)

    gene_strand = '-'

    info_columns = ['strand', 'gRNA', 'off_target_summary', 'location']

    edits = []
    bec, bea = CytidineDeaminase(), AdenineDeaminase()
    for strand, guide, offtarget, location in glib[info_columns].values:
        for be in [bec, bea]:
            chrm, start, end = be.parse_coordinates(location)
            guide_edited = be.edit_guide(guide, strand, gene_strand)

            print(f'# {be.name}, {chrm}:{start}-{end}:')
            print(f'Guide strand: {strand}, Gene strand: {gene_strand}')

            bec.print_guide(guide)
            bec.print_guide(guide_edited)

            guide_edits = be.to_vep(guide, guide_edited)

            if guide_edits is not None:
                guide_vep = dict(
                    chr=chrm,
                    start=start + guide_edits[1],
                    end=start + guide_edits[2],
                    edit=guide_edits[0],
                    strand='-'
                )
                edits.append(guide_vep)
                print(guide_vep)

        print('\n')

    # -
    edits_df = pd.DataFrame(edits)[['chr', 'start', 'end', 'edit', 'strand']]
    edits_df.to_csv('/Users/eg14/Downloads/WGE_JAK1_vep_input.txt', sep='\t', index=False, header=False)

    # -
    vep = pd.read_csv('/Users/eg14/Downloads/WGE_JAK1_vep_output.txt', sep='\t').dropna(subset=['Amino_acids'])
    vep = vep[vep['CSN'].apply(lambda v: v.startswith('ENST00000342505.4'))]

    ptms = vep[vep['Amino_acids'].apply(lambda v: '/' in v)]

    ptms['site'] = \
        ptms['Amino_acids'].apply(lambda v: v[0]) + \
        ptms['Protein_position'].astype(str)

    ptms['residue'] = \
        ptms['Amino_acids'].apply(lambda v: v[0]) + \
        ptms['Protein_position'].astype(str) + \
        ptms['Amino_acids'].apply(lambda v: v[-1:])

    #
    sift = ptms['SIFT'].apply(lambda v: v.split('(')[0]).value_counts()
    pholyphen = ptms['PolyPhen'].apply(lambda v: v.split('(')[0]).value_counts()
    consequence = pd.Series([i for i in ptms['Consequence'] if ',' not in i]).value_counts()

    #
    phosphosites = ptms[[i[0] in ['S', 'T', 'Y'] for i in ptms['Amino_acids']]]
    methylation = ptms[[i[0] in ['K', 'R'] for i in ptms['Amino_acids']]]

