import pybedtools as pbt
import Bio
from Bio.Seq import Seq


class Extraction_of_data:
    def extract(self):
        pass


class Gtf_helper():

    def __init__(self, name_of_file):
        self.name_of_file = name_of_file

        self.input_of_start_and_end = 0

    def extract_window_from_gene_id(self, gene_ID):
        with open(self.name_of_file) as gff:
            for line in gff:
                line = line.strip()
                name_of_element = '"' + gene_ID + '"'
                a = line.find(name_of_element)

                if a != -1:
                    line = line.split('\t')


                    if line[2] == 'gene':
                        self.find = 1
                        start_of_gene = (int(line[3]) - 1)
                        end_of_gene = int(line[4])
                        name_of_scaffold = line[0]
        if self.find == 1:
            #gene_info = dict(start_of_gene=start_of_gene, end_of_gene=end_of_gene, name_of_scaffold=name_of_scaffold)
            gene_info = [name_of_scaffold, start_of_gene, end_of_gene]
            return (gene_info)
        else:
            print('Gene not found')
            exit()

    def extract_transcripts_from_widnow(self, chr, start, end, selected_transcripts = 0):

        self.input_of_start_and_end = 1
        self.scaffold = chr
        self.start = int(start)
        self.end = int(end)
        with open(self.name_of_file) as gff:
            transcripts = []
            for line in gff:
                line = line.strip()
                line = line.split('\t')

                if line[0] == self.scaffold and line[2] == 'transcript' and (
                        (self.start <= int(line[3]) <= int(line[4]) <= self.end) or (
                        int(line[3]) <= self.start <= self.end <= int(line[4])) or (
                                self.start <= int(line[3]) < self.end) or (self.start < int(line[4]) <= self.end)):

                    needed_data = line[8].split(';')[1].split('"')[1]
                    if transcripts.count(needed_data) == 0:
                        transcripts.append(needed_data)
        new_transcripts = []
        if selected_transcripts != 0:
            for i in selected_transcripts:
                if i in transcripts:
                    new_transcripts.append(i)
        else:
            new_transcripts = transcripts
        transcripts = new_transcripts

        return (transcripts)


    def extract_data_about_transcripts(self, elements_id, users_scaffold=0, users_start=0, users_end=0):
        if len(elements_id) == 0:
            for_transcript = []
            data = dict(exons='0-0', CDS='0-0', start_of_transcript=0, end_of_transcript=0, strand='(+)', start_codon=0,
                        name_of_transcript='no annotated transcripts in the window', stop_codon=0)
            for_transcript.append(data)

            data_from_gff = dict(for_transcript=for_transcript, name_of_scaffold=self.scaffold, start=self.start,
                                 end=self.end)
            return (data_from_gff)

        if users_start and users_end and users_scaffold != 0:
            self.input_of_start_and_end = 1
            self.start = users_start
            self.end = users_end
            self.scaffold = users_scaffold

        full_data = []

        if type(elements_id) == str:
            elements_id = elements_id.split(',')
        for name_of_element in elements_id:

            self.name_of_element = name_of_element
            self.exist = 0
            exons = ''
            CDS = ''
            strand = ''
            start_and_stop = []
            with open(self.name_of_file) as gff:
                gff = gff
                name_of_element = '"' + name_of_element + '"'
                for line in gff:
                    line = line.strip()

                    a = line.find(name_of_element)

                    if a != -1:
                        self.exist = 1

                        line = line.split('\t')
                        if line[2] == 'CDS':
                            CDS += str(int(line[3]) - 1) + '-' + line[4] + ';'
                            start_and_stop.append(int(line[3]) - 1)
                            start_and_stop.append(int(line[4]))

                        if line[2] == 'exon':
                            exons += str(int(line[3]) - 1) + '-' + line[4] + ';'
                        if line[2] == 'transcript':
                            start_of_transcript = (int(line[3]) - 1)
                            end_of_transcript = int(line[4])
                            name_of_scaffold = line[0]
                            strand = '(' + line[6] + ')'

                CDS_row = CDS.split(';')
                CDS = ''
                for i in CDS_row:
                    if i != '':
                        CDS += i
                        if i != CDS_row[::-1][1]:
                            CDS += ';'

                exons_row = exons.split(';')
                exons = ''
                for i in exons_row:
                    if i != '':
                        exons += i
                        if i != exons_row[::-1][1]:
                            exons += ';'

                if self.exist == 1:
                    if strand == '(+)' and len(start_and_stop) != 0:
                        start_codon = min(start_and_stop)
                        stop_codon = max(start_and_stop)
                    elif strand == '(-)' and len(start_and_stop) != 0:
                        start_codon = max(start_and_stop) - 2
                        stop_codon = min(start_and_stop)
                    else:
                        start_codon = start_of_transcript
                    self.start_of_transcript = start_of_transcript
                    self.end_of_transcript = end_of_transcript

                    data_from_gff = dict(exons=exons, CDS=CDS, start_of_transcript=start_of_transcript,
                                         end_of_transcript=end_of_transcript, strand=strand, start_codon=start_codon,
                                         name_of_transcript=self.name_of_element)
                    full_data.append(data_from_gff)
        if self.exist ==1:
            if self.input_of_start_and_end == 1:
                data_from_gff = dict(for_transcript=full_data, name_of_scaffold=self.scaffold, start=self.start,
                                     end=self.end)
            else:

                data_from_gff = dict(for_transcript=full_data, name_of_scaffold=name_of_scaffold, start=start_of_transcript,
                                     end=end_of_transcript)
            return (data_from_gff)
        else:
            print('Transcripts not found')
            exit()


    def extract_data_around_ts(self, transcript_id, window, selected_transcripts = 0):
        data_from_gtf = self.extract_data_about_transcripts(transcript_id)


        if window[0] == 'tis':
            start = data_from_gtf['for_transcript'][0]['start_codon'] - int(window[1])
            end = data_from_gtf['for_transcript'][0]['start_codon'] + int(window[2])
            scaffold = data_from_gtf['name_of_scaffold']
            transcripts = self.extract_transcripts_from_widnow(scaffold, start, end, selected_transcripts)

            data_from_gtf = self.extract_data_about_transcripts(transcripts)

        elif window == 'tts':

            start = data_from_gtf['for_transcript'][0]['start_of_transcript'] - int(window)
            end = data_from_gtf['for_transcript'][0]['start_of_transcript'] + int(window[2])
            scaffold = data_from_gtf['name_of_scaffold']
            transcripts = self.extract_transcripts_from_widnow(scaffold, start, end, selected_transcripts)
            data_from_gtf = self.extract_data_about_transcripts(transcripts)

        return  data_from_gtf
class Extraction_of_sequence(Extraction_of_data):

    def __init__(self, name_of_file, name_of_scaffold, start, end):
        self.name_of_file = name_of_file
        self.name_of_scaffold = name_of_scaffold
        self.start = start
        self.end = end

    def extract(self):
        name_of_scaffold, start, end = self.name_of_scaffold, self.start, self.end
        a = pbt.BedTool("%s\t%i\t%i" % (name_of_scaffold, start, end), from_string=True)
        fasta = self.name_of_file
        a = a.sequence(fi=fasta)
        sequence = open(a.seqfn).read().split('\n')[1]

        return (sequence)


class Extraction_of_coverage(Extraction_of_data):

    def __init__(self, name_of_file, name_of_scaffold, start, end):

        self.name_of_file = name_of_file
        self.name_of_scaffold = name_of_scaffold
        self.start = start
        self.end = end

    def extract(self):

        with open(self.name_of_file) as bedgraph:

            pos_of_start = []
            length_of_interval = []
            self.found = 0
            coverage_on_interval = []
            for line in bedgraph:
                line = line.strip()
                line = line.split('\t')

                if line[0] == self.name_of_scaffold and (int(line[1]) >= self.start) and (int(line[2]) <= self.end):
                    pos_of_start.append(int(line[1]) - self.start)
                    length_of_interval.append(int(line[2]) - int(line[1]))
                    coverage_on_interval.append(int(line[3]))
                    self.found = 1

            if self.found == 0:
                if 'chr' in self.name_of_scaffold:
                    self.name_of_scaffold = self.name_of_scaffold[3::]
                else:
                    self.name_of_scaffold = 'chr' + self.name_of_scaffold
            for line in bedgraph:
                line = line.strip()
                line = line.split('\t')

                if line[0] == self.name_of_scaffold and (int(line[1]) >= self.start) and (int(line[2]) <= self.end):
                    pos_of_start.append(int(line[1]) - self.start)
                    length_of_interval.append(int(line[2]) - int(line[1]))
                    coverage_on_interval.append(int(line[3]))



        coverage = [0 for i in range(self.end - self.start)]
        for i in range(len(pos_of_start)):
            for q in range(length_of_interval[i]):
                coverage[pos_of_start[i] + q] = coverage_on_interval[i]

        coverage_str = ''
        count = 0
        for i in coverage:
            count += 1
            coverage_str += str(i)
            if count != len(coverage):
                coverage_str += ','
        coverage_str = dict(coverage_str=coverage_str)

        return (coverage_str)
