#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:04:08 2018

@author: antony
"""

import collections
import libdna

CHECK = 42
VERSION = 1

GENE_NAME = 'gene_name'
GENE_ID = 'gene_id'


GENE = 'gene'
TRANSCRIPT = 'transcript'
EXON = 'exon'


def overlap(chr1, start1, end1, chr2, start2, end2):
    if chr1 != chr2 or end1 < start2 or end2 < start1:
        return None

    start = max(start1, start2)
    end = min(end1, end2)

    return libdna.Loc(chr, start, end)


class GenomicEntity(libdna.Loc):
    def __init__(self, chr, start, end, level, strand, ann_map = None):
        super().__init__(chr, start, end)
        
        if ann_map is None:
            ann_map = {}
        
        self.__level = level
        self.__strand = strand
        self.__ann_map = ann_map
        self.__tags = set()
        self.__children = collections.defaultdict(list)
    
    @property    
    def level(self):
        return self.__level
    
    @property
    def strand(self):
        return self.__strand
    
    def add(self, e):
        self.__children[e.level].append(e)
        
    def child_levels(self):
        return sorted(self.__children.keys())
    
    def children(self, level):
        return self.__children[level]
    
    def child_count(self, level):
        return len(self.__children[level])
    
    def tag_count(self):
        return len(self.__tags)
    
    def set_annotation(self, name, value):
        self.__ann_map[name] = value
        
    def set_id(self, name, value):
        self.set_annotation(name, value)
        
    def set_ids(self, ids):
        for key, value in ids.items():
            self.__ann_map[key] = value
    
    def annotation_names(self):
        return sorted(self._ann_map.keys())
    
    def annotation(self, name):
        if name in self.__ann_map:
            return self.__ann_map[name]
        else:
            return ''
    
    @property
    def ids(self):
        return self.__ann_map
    
    @property
    def annotations(self):
        return self.__ann_map
    
    def annotation_count(self):
        return len(self.__ann_mapp)
    
    def _ann_str(self):
        ret = []
        
        for key in sorted(self.__ann_map):
            ret.append('{}="{}"'.format(key, self.__ann_map[key]))
            
        return ';'.join(ret)
    
    @property
    def tags(self):
        return sorted(self.__tags)
    
    def add_tag(self, tag):
        self.__tags.add(tag)
        
    def add_tags(self, tags):
        for tag in tags:
            self.__tags.add(tag)
    
    def _tags_str(self):
        return ';'.join(sorted(self.__tags))
    
    @property
    def gene_name(self):
        return self.annotation(GENE_NAME)
    
    @property
    def symbol(self):
        return self.gene_name
    
    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}'.format(super().__str__(), self.level, self.strand, self._ann_str(), self._tags_str())
    
    @staticmethod
    def chr_map(entities):
        chr_map = collections.defaultdict(list)
        
        for e in entities:
            chr_map[e.chr].append(e)
            
        return chr_map


class Exon(GenomicEntity):
    def __init__(self, chr, start, end, strand):
        super().__init__(chr, start, end, EXON, strand)
        
   
    def add_exon(self, exon):
        if exon.level == EXON:
            self.add(exon)
            
    def exons(self):
        return self.children(EXON)
    

class Transcript(GenomicEntity):
    def __init__(self, chr, start, end, strand):
        super().__init__(chr, start, end, TRANSCRIPT, strand)
        
    def add_exon(self, exon):
        if exon.level == EXON:
            self.add(exon)
            
    def exons(self):
        return self.children(EXON)


class Gene(GenomicEntity):
    def __init__(self, chr, start, end, strand):
        super().__init__(chr, start, end, GENE, strand)
   
    def add_exon(self, exon):
        if exon.level == TRANSCRIPT:
            self.add(exon)
            
    def transcripts(self):
        return self.children(TRANSCRIPT)


class Genes(object):
    pass
    
class SingleDBGenes(Genes):
    def __init__(self, db, genome):
        self.__db = db
        self.__genome = genome
        
    @property
    def db(self):
        return self.__db
    
    @property
    def genome(self):
        return self.__genome