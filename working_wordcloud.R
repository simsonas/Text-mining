#library(twitteR)
library(NLP)
library(tm)
library(RColorBrewer)
library(wordcloud)


library(ggplot2)

setwd ("c:/sentiment")

mach_text = readLines("test.txt")

#kazka padariau dfafasdfaf
#hello world
mach_text = reviews

# create a corpus
mach_corpus = Corpus(VectorSource(mach_text))

# create document term matrix applying some transformations
tdm = TermDocumentMatrix(mach_corpus,
                         control = list(removePunctuation = TRUE,
                                        #stopwords = c("draudimas", "kad","tai", stopwords("english")),
                                        stopwords1 = c(stopw,"draudime", "dabar", "tada", "tikrai", "draudimas", "draudimo", "buvo", "lietuvos", "jie", "jau", "draudimu", "cia", "yra", "draudima", "reikia", "metu", "nieko"),
                                        removeNumbers = TRUE, tolower = TRUE))
# define tdm as matrix
m = as.matrix(tdm)
# get word counts in decreasing order
word_freqs = sort(rowSums(m), decreasing=TRUE) 
# create a data frame with words and their frequencies
dm = data.frame(word=names(word_freqs), freq=word_freqs)

colorPalette <- brewer.pal(8, "RdBu")


# plot wordcloud
wordcloud(dm$word, dm$freq, random.order=FALSE, min.freq=3, rot.per=0.2, scale=c(3, .2), colors=brewer.pal(8, "RdBu"))

# save the image in png format
png("draudimas.png", width=12, height=8, units="in", res=300, bg="black")
wordcloud(dm$word, dm$freq, random.order=FALSE, min.freq=3, rot.per=0.2, scale=c(3, .2), colors=brewer.pal(8, "RdBu"))
#wordcloud(dm$word, dm$freq, random.order=FALSE, colors=brewer.pal(8, "Dark2"))

dev.off()
