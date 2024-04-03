args = commandArgs(trailingOnly=TRUE)

if (length(args) != 1)
    stop("An input BLASTp file is required.")

seqs <- read.table(args[1], sep="\t", stringsAsFactors=F, comment.char="", header=F)
names(seqs) <- c("qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore","qcovs")
seqs
#sort by percent identity so you can get the best hit for each gene
order_seqs <- seqs[order(-seqs$pident),]
#remove duplicates - this keeps the first instance which will be higher since they were sorted
uniq_hpw <- order_seqs[!duplicated(order_seqs$qseqid),]

# work w/ input filename string to make output filename
outfile <- gsub("\\..*","",args[1])

write.table(uniq_hpw, row.names=FALSE, quote=FALSE, sep='\t', file=paste(outfile, ".filtered_best_hits.txt", sep=''))

