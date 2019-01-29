library("dplyr")
library("stringr")
library("Biostrings")

getGeneLocs <- function(gff_file){
  gff = read.delim("directory of GFF file", header=F, comment.char="#")
  gff = dplyr::filter(gff, grepl("gene", V3, fixed=TRUE))
  gff2 = gff[gff$V3=="gene",]
  gff2 = gff2[!duplicated(gff2$V4),]
  gene_start_locs = gff2$V4
  gene_end_locs = gff2$V5
  gene_orientation = as.character(gff2$V7)
  gene_names = as.character(gff2$V9)
  gene_names = unlist(strsplit(gene_names, ";"))
  gene_names = gene_names[str_detect(gene_names, "gene=")]
  gene_names = gsub("gene=","", gene_names)
  output = list(start=gene_start_locs, name=gene_names, end=gene_end_locs, orien=gene_orientation)
  write.csv(output,file = "clean_gff.csv")
}

