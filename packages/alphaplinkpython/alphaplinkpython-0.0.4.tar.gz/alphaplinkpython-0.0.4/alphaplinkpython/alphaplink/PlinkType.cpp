//
// Created by david on 25/06/2018.
//

#include "PlinkType.h"

using namespace PlinkType;

Snp::Snp(std::vector<string> in)
{

if (in.size() < 6)
return;

chrom = std::stoi(in[0]);
name = in[1];
basepair = std::stoi(in[2]);
number = std::stoi(in[3]);
refAllele = in[4];
altAllele = in[5];
}

bool Snp::operator==(const Snp& other) {
    if (chrom != other.chrom) return false;
    if (name != other.name)
        return false;
    if (basepair != other.basepair)
        return false;
    if (number != other.number)
        return false;
    if (refAllele != other.refAllele)
        return false;
    if (altAllele != other.altAllele)
        return false;

    return true;
}

Snp::Snp(int chrom, string name, int basepair, int number, string refAllele, string altAllele)
{

    this->chrom = chrom;
    this->name = name;
    this->basepair = basepair;
    this->number = number;
    this->refAllele = refAllele;
    this->altAllele = altAllele;
}




BimType::BimType()
{
    chromosomes = std::vector<std::shared_ptr<Chromosome>>();
    snps = std::vector<snp_ptr>();
}

BimType::BimType(int totalSnps, std::vector<int> nsnpsPerChrom)
{

    string baseName = "snp";
    int basePair = 0;

    string refAllele = "A";
    string altAllele = "B";

    int chromCount = 0;
    int snpsInChrom = 0;
    snps = std::vector<snp_ptr>();

    for (int i = 0; i < totalSnps; i++)
    {
        snpsInChrom++;
        snps.push_back(std::make_shared<Snp>(chromCount + 1, baseName + std::to_string(i), basePair, i, refAllele, altAllele));
        if (snpsInChrom == nsnpsPerChrom[chromCount])
        {
            chromCount++;
            snpsInChrom = 0;
        }
    }
}

std::vector<string> PlinkType::splitString(const string &word, const char delim)
{
    std::vector<string> ret = {};
    string cur = "";

    for (int i=0; i<word.size(); i++ ) {

        if (word[i] == delim) {

            if (!cur.empty()) {
                ret.push_back(cur);
                cur="";
            }
        }
        else {
            cur +=  word[i];
        }
    }
    if (!cur.empty()) {
        ret.push_back(cur);
    }
    return ret;

}

bool PlinkType::getBit(unsigned char byte, int position) // position in range 0-7
{
    return (byte >> position) & 0x1;
}


bool Chromosome::operator==(const Chromosome& other) {
        if (snps.size() != other.snps.size()) return false;
        
        return std::equal(snps.begin(), snps.end(), other.snps.begin(),
                [](const snp_ptr lhs, const snp_ptr rhs){ return *lhs == * rhs; });
    }


bool BimType::operator==(const BimType& other) {

        if (snps.size() != other.snps.size()) return false;
        if (!std::equal(snps.begin(), snps.end(), other.snps.begin(),
                [](const snp_ptr lhs, const snp_ptr rhs){ return *lhs == * rhs; }))
            return false;

        if (chromosomes.size() != other.chromosomes.size()) return false;
        if (!std::equal(chromosomes.begin(), chromosomes.end(), other.chromosomes.begin(),
                [](const std::shared_ptr<Chromosome> lhs, const std::shared_ptr<Chromosome> rhs){ return *lhs == * rhs; }))
            return false;

        return true;
    }
bool FamObject::operator==(const FamObject &other)
    {
        if (familyId != other.familyId) return false;
        if (id != other.id) return false;
        if (sire != other.sire) return false;
        if (dam != other.dam) return false;
        if (gender != other.gender) return false;
        if (phen != other.phen) return false;
        return true;
    }


bool FamType::operator==(const FamType &other) {

         if (ped.size() != other.ped.size()) return false;
         return std::equal(ped.begin(), ped.end(), other.ped.begin(),
                [](const std::shared_ptr<FamObject> lhs, const std::shared_ptr<FamObject> rhs){ return *lhs == * rhs; });

     }


     bool PlinkHolder::operator==(const PlinkHolder &other) {
        if ( bed != other.bed) return false;

        if (bim != other.bim) return false;

        if (fam != other.fam) return false;


        return true;
}