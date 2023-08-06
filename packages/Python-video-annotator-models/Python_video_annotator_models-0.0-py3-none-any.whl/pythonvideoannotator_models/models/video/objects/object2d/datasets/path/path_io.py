import os, csv, math
from pythonvideoannotator_models.models.video.objects.object2d.datasets.path.path_base import PathBase

class PathIO(PathBase):

    FACTORY_FUNCTION = 'create_path'


    ######################################################################################
    #### IO FUNCTIONS ####################################################################
    ######################################################################################

    def save(self, data, dataset_path=None):
        #data = super(PathIO, self).save(data, dataset_path)

        dataset_file = os.path.join(dataset_path, 'path.cvs')
        with open(dataset_file, 'wb') as outfile:
            outfile.write((';'.join(['frame','x','y'])+'\n').encode())
            for index in range(len(self)):
                pos = self.get_position(index, use_referencial=False)
                row = [index] + ([None, None] if pos is None else list(pos))
                outfile.write((';'.join( map(str,row) )).encode( ))
                outfile.write(b'\n')

        # save the referencial data
        data['apply-referencial'] = self.apply_referencial
        data['referencial-point'] = self.referencial


        super(PathIO,self).save(data, dataset_path)
        return data

    def load(self, data, dataset_path=None):
        data = super(PathIO, self).load(data, dataset_path)
        
        dataset_file = os.path.join(dataset_path, 'path.cvs')   

        with open(dataset_file, 'rb') as infile:
            infile.readline()
            for i, line in enumerate(infile):
                csvrow = line[:-1].split(b';')

                if csvrow[1] is None or csvrow[2] is None:      continue
                if len(csvrow[1])==0 or len(csvrow[2])==0:      continue
                if csvrow[1] == b'None' or csvrow[2] == b'None':continue
                
                frame, x, y = int(csvrow[0]), int(csvrow[1]), int(csvrow[2])
                self.set_position(frame, x, y)

        # load the referencial data
        ref                     = data.get('referencial-point', None)
        self.referencial        = tuple(ref) if ref else None
        self.apply_referencial  = data.get('apply-referencial', False)

        return data



    def import_csv(self, filename, first_row=0, col_frame=0, col_x=1, col_y=2):

        with open(filename, 'U') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(2048))
            csvfile.seek(0)
            spamreader = csv.reader(csvfile, dialect)
            
            for i in range(first_row): next(spamreader, None)  # skip the headers

            count = 0
            
            for row in spamreader:
                if len(row)==0: break
                if col_frame<0:
                    x, y  = row[col_x], row[col_y]
                    frame = count
                    count += 1
                else:
                    frame, x, y = row[col_frame], row[col_x], row[col_y]
                    frame = int(frame)
                x = None if x=='None' or x.strip()=='' else float(x)
                y = None if y=='None' or y.strip()=='' else float(y)

                if x is not None and y is not None and not math.isnan(x) and not math.isnan(y):
                    self.set_position(frame, int(round(x,0)), int(round(y,0)))