/** @file PseudoMultiAlign.C
 *
 *   File:  PseudoMultiAlign.C
 *   Date:  Sep 03, 2018 ZF
 *
 *  Implementation of local pairwise alignment utilties.
 *  Adapts the particular code from Smith-Waterman local alignment algorithm 
 *  from RCSB Maxit (Z. Feng).  A simplified binary scoring function is used
 *  to address the problem of aligning reference, author supplied and coordinate
 *  sequences. 
 *
 *  Methods are provided to manage and align multiple pairwise alignments from
 *  to a common reference sequence.
 *
 *  AlignUtil.h & AlignUtil.C were directly copied from annotation-pack/utillib module.
 *  PseudoMultiAlign is the modified verion of PseudoMultiAlign class from annotation-pack/utillib module.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <iomanip>

#include "AlignUtil.h"
#include "PseudoMultiAlign.h"

#define VV  2
#define UU  1

using namespace RCSB;

typedef struct {
        std::vector<std::string> seqa;
        std::vector<std::string> seqb;
} _DataContainer;

static std::string gapSymbol = ".";

static double coord_score(const int& i, const int& j, void* data);
static double ref_score(const int& i, const int& j, void* data);
static double auth_score(const int& i, const int& j, void* data);

PseudoMultiAlign::PseudoMultiAlign()
{
       clear();
}

PseudoMultiAlign::~PseudoMultiAlign()
{
       clear();
}

void PseudoMultiAlign::clear()
{
       _factor = 10;
       _uu = UU;
       _vv = VV;
       _sfunc = &coord_score;
       _authSeq.clear();
       _internal_align_indices.clear();
       _public_align_indices.clear();
       _align_sequences.clear();
}

void PseudoMultiAlign::setPenaltyFactor(const double& value)
{
       _factor = value;
}

void PseudoMultiAlign::setRefScore()
{
       _uu = UU;
       _vv = VV;
       _sfunc = &ref_score;
}

void PseudoMultiAlign::setAuthScore()
{
       _uu = 0;
       _vv = 0;
       _sfunc = &auth_score;
}

void PseudoMultiAlign::setAuthSequence(const std::vector<std::vector<std::string> >& seqs)
{
       std::vector<int> index, auth_indices, embed_linkage;
       std::vector<std::string> seqList;
       _get_seq_index_linkage_info(seqs, _authSeq, auth_indices, embed_linkage);

       index.clear(); index.push_back(0);
       seqList.clear(); seqList.push_back(gapSymbol);

       for (unsigned int i = 0; i < _authSeq.size(); ++i) {
            index[0] = i;
            _internal_align_indices.push_back(index);

            index[0] = auth_indices[i];
            _public_align_indices.push_back(index);

            seqList[0] = _authSeq[i];
            _align_sequences.push_back(seqList);
       }
}

void PseudoMultiAlign::addAlignSequence(const std::vector<std::vector<std::string> >& seqs)
{
       std::vector<std::string> embed_seqs;
       std::vector<int> auth_indices, embed_linkage;
       _get_seq_index_linkage_info(seqs, embed_seqs, auth_indices, embed_linkage);
       _multiple_alignment(embed_seqs, auth_indices, embed_linkage);
}

void PseudoMultiAlign::addAlignSequenceWithRange(const std::vector<std::vector<std::string> >& seqs, const unsigned int& begin, const unsigned int& end)
{
       std::vector<std::string> embed_seqs;
       std::vector<int> auth_indices, embed_linkage;
       _get_seq_index_linkage_info(seqs, embed_seqs, auth_indices, embed_linkage);
       _multiple_alignment(embed_seqs, auth_indices, embed_linkage, begin, end);
}

void PseudoMultiAlign::addAlignSequenceWithLinkageAndRange(const std::vector<std::vector<std::string> >& seqs, const std::vector<int>& linkage,
                                                           const unsigned int& begin, const unsigned int& end)
{
       std::vector<std::string> embed_seqs;
       std::vector<int> auth_indices, embed_linkage;
       _get_seq_index_linkage_info(seqs, embed_seqs, auth_indices, embed_linkage);
       _multiple_alignment(embed_seqs, auth_indices, linkage, begin, end);
}

std::vector<std::vector<int> > PseudoMultiAlign::getAlignIndices()
{
       return _public_align_indices;
}

std::vector<std::vector<std::string> > PseudoMultiAlign::getAlignSequences()
{
       return _align_sequences;
}

void PseudoMultiAlign::_get_seq_index_linkage_info(const std::vector<std::vector<std::string> >& input_seqs, std::vector<std::string>& output_seqs,
                                                   std::vector<int>& auth_indices, std::vector<int>& embed_linkage)
{
       output_seqs.clear();
       auth_indices.clear();
       embed_linkage.clear();
       for (std::vector<std::vector<std::string> >::const_iterator vpos = input_seqs.begin(); vpos != input_seqs.end(); ++vpos) {
            output_seqs.push_back((*vpos)[0]);
            if (vpos->size() >= 2) auth_indices.push_back(atoi((*vpos)[1].c_str()));
            if (vpos->size() >= 3) embed_linkage.push_back(atoi((*vpos)[2].c_str()));
       }

       if (auth_indices.size() != output_seqs.size()) {
            auth_indices.clear();
            for (unsigned int i = 0; i < output_seqs.size(); ++i) auth_indices.push_back(i);
       }

       if (embed_linkage.size() != output_seqs.size()) embed_linkage.clear();
} 

void PseudoMultiAlign::_multiple_alignment(const std::vector<std::string>& seqb, const std::vector<int>& auth_indices, const std::vector<int>& linkage,
                                           const unsigned int& begin_orig, const unsigned int& end_orig)
{
       _DataContainer cdata;
       unsigned int begin = _getConsensusSeq(cdata.seqa, begin_orig, end_orig, 10);
       cdata.seqb = seqb;

       std::vector<std::vector<int> > ss, sa, sb;

       AlignUtil::initAssignment(sa, cdata.seqa.size());
       AlignUtil::initAssignment(sb, cdata.seqb.size());

       AlignUtil::Alignment(ss, sa, sb, _vv, _uu, _sfunc, (void*) &cdata, linkage, _factor);

       if (begin) {
            unsigned int count = 0;
            for (unsigned int i = 0; i < ss.size(); ++i) {
                 if (ss[i][0] >= 0) break;
                 count++;
            }
            if (count) {
                 begin = _getConsensusSeq(cdata.seqa, begin_orig, end_orig, count + 10);
                 AlignUtil::Alignment(ss, sa, sb, _vv, _uu, _sfunc, (void*) &cdata, linkage, _factor);
            }
       }

       std::vector<std::vector<int> > result_internal_align_indices, result_public_align_indices;
       result_internal_align_indices.clear();
       result_internal_align_indices.reserve(begin + ss.size());
       result_public_align_indices.clear();
       result_public_align_indices.reserve(begin + ss.size());

       std::vector<std::vector<std::string> > result_align_sequences;
       result_align_sequences.clear();
       result_align_sequences.reserve(begin + ss.size());

       std::vector<int> index, public_index;
       std::vector<std::string> seq;

       for (unsigned int i = 0; i < begin; ++i) {
            index = _internal_align_indices[i];
            index.push_back(-1);
            result_internal_align_indices.push_back(index);

            public_index = _public_align_indices[i];
            public_index.push_back(-1);
            result_public_align_indices.push_back(public_index);

            seq = _align_sequences[i];
            seq.push_back(gapSymbol);
            result_align_sequences.push_back(seq);
       }


       for (unsigned int i = 0; i < ss.size(); ++i) {
            if (ss[i][0] >= 0) {
                 index = _internal_align_indices[ss[i][0] + begin];
                 public_index = _public_align_indices[ss[i][0] + begin];
                 seq = _align_sequences[ss[i][0] + begin];
                 if (ss[i][1] >= 0) {
                      index.push_back(ss[i][1]);
                      public_index.push_back(auth_indices[ss[i][1]]);
                      seq.push_back(seqb[ss[i][1]]);
                 } else {
                      index.push_back(-1);
                      public_index.push_back(-1);
                      seq.push_back(gapSymbol);
                 }
            } else {
                 index.clear();
                 public_index.clear();
                 seq.clear();
                 for (unsigned int j = 0; j < _internal_align_indices[0].size(); ++j) {
                      index.push_back(-1);
                      public_index.push_back(-1);
                      seq.push_back(gapSymbol);
                 }
                 index.push_back(ss[i][1]);
                 public_index.push_back(auth_indices[ss[i][1]]);
                 seq.push_back(seqb[ss[i][1]]);
            }

            result_internal_align_indices.push_back(index);
            result_public_align_indices.push_back(public_index);
            result_align_sequences.push_back(seq);
       }

       _internal_align_indices = result_internal_align_indices;
       _public_align_indices = result_public_align_indices;
       _align_sequences = result_align_sequences;
}


unsigned int PseudoMultiAlign::_getConsensusSeq(std::vector<std::string>& seqs, const unsigned int& begin_orig, const unsigned int& end_orig,
                                                             const unsigned int& extra)
{
       unsigned int begin = 0;
       if (begin_orig && end_orig) {
            unsigned int start_num = 1;
            if (begin_orig > extra) start_num = begin_orig - extra;

            bool found_begin = false, found_end = false;
            for (unsigned int i = 0; i < _public_align_indices.size(); ++i) {
                 if (_public_align_indices[i][0] == ((int) start_num - 1)) {
                      begin = i;
                      found_begin = true;
                 } else if (_public_align_indices[i][0] == ((int) end_orig - 1)) {
                      found_end = true;
                      if (found_begin) break;
                 }
            }
            if (!found_begin || !found_end) begin = 0;
       }

       seqs.clear();
       seqs.reserve(_align_sequences.size() - begin);

       for (unsigned int i = begin; i < _align_sequences.size(); ++i) {
            std::string res = gapSymbol;
            if (_align_sequences[i][0] != gapSymbol)
                 res = _align_sequences[i][0];
            else {
                 for (unsigned int k = 1; k < _align_sequences[i].size(); ++k) {
                      if (_align_sequences[i][k] != gapSymbol) {
                           res = "-" + _align_sequences[i][k];
                           break;
                      }
                 }
            }
            seqs.push_back(res);
       }

       return begin;
}

static double coord_score(const int& i, const int& j, void* data)
{
       _DataContainer *cdata = (_DataContainer*) data;

       bool consensusFlag = false;
       std::string resName = cdata->seqa[i];
       if (resName[0] == '-') {
            resName = cdata->seqa[i].substr(1);
            consensusFlag = true;
       }

       if (resName == gapSymbol) return 0;

       if (resName != cdata->seqb[j])
            return 0;
       else if (consensusFlag) {
            if (resName == "ALA")
                 return 1;
            else return 3;
       } else {
            if (resName == "ALA")
                 return 2;
            else return 5;
       }
}

static double ref_score(const int& i, const int& j, void* data)
{
       _DataContainer *cdata = (_DataContainer*) data;

       bool consensusFlag = false;
       std::string resName = cdata->seqa[i];
       if (resName[0] == '-') {
            resName = cdata->seqa[i].substr(1);
            consensusFlag = true;
       }

       if (resName == gapSymbol) return 0;

       if (resName != cdata->seqb[j])
            return 0;
       else if (consensusFlag) {
            if (resName == "ALA")
                 return 1;
            else return 3;
       } else {
            if (resName == "ALA")
                 return 2;
            else return 5;
       }
}

static double auth_score(const int& i, const int& j, void* data)
{
       _DataContainer *cdata = (_DataContainer*) data;

       bool consensusFlag = false;
       std::string resName = cdata->seqa[i];
       if (resName[0] == '-') {
            resName = cdata->seqa[i].substr(1);
            consensusFlag = true;
       }

       if (resName != cdata->seqb[j]) {
            if ((resName == gapSymbol) || (cdata->seqb[j] == gapSymbol))
                 return (-5);
            else return 0;
       } else if (resName == gapSymbol)
            return 0;
       else if (consensusFlag)
            return 3;
       else return 5;
}
