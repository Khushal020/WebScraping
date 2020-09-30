import pandas as pd

fake = pd.read_csv('news_content_fake.csv')
#print(fake)
fake['tag'] = 'fake'
#print(fake)

real = pd.read_csv('news_content_real.csv')
real['tag'] = 'real'
#print(real)

frames = [fake, real]
final = pd.concat(frames)
print(final.head())
print(final.tail())

final.to_csv('politifact.csv')

