import binarizer as bin


bible = 'Goettingen'
read_path = 'GenesisPages/old/{bible}'.format(bible=bible)
save_path = 'GenesisPages/old/{bible}_binarized'.format(bible=bible)

binar = bin.Binarizer(bible, read_path, save_path)
binar.binarize()
