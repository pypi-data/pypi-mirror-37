//
// Created by david on 18/05/2018.
//

#include <boost/iostreams/device/mapped_file.hpp> // for mmap
#include <boost/iostreams/stream.hpp>             // for stream
#include <boost/dynamic_bitset.hpp>               // for stream
#include <boost/algorithm/string/replace.hpp>     // for stream
// #include <boost/filesystem.hpp>
#include <algorithm> // for std::find
#include <iostream>  // for std::cout
#include <cstring>
#include <vector>
#include <boost/integer.hpp>
#include <iostream> // std::cout
#include <fstream>  // std::ifstream
#include <cstdint>
#include <array>
#include <memory>
#include <string>
#include "PlinkType.h"
#include "PlinkWriter.h"
#include "BitHolder.h"
#include <cstdio>
#include <bitset>

using std::string;
using std::vector;

const int MISSINGCODE = 9;
using namespace PlinkType;

int countLines(string fileName)
{
    std::ifstream file(fileName);
    string line;
    int count = 0;
    while (getline(file, line))
        count++;
    return count;
}
// simple function to return if file exists
bool doesFileExist(const char *fileName)
{
    std::ifstream infile(fileName);
    return infile.good();
}

/**
 * Function deletes filestart.bed and filestart.bim files from working directory
 */
void removeFiles(const string &fileStart)
{
    int val = 0;

    string temp = fileStart + ".bed";
    val = std::remove(temp.c_str());
    if (!val) {
        std::cout << "deleted " << (fileStart + ".bed") << '\n';
    }
    temp = fileStart + ".bim";
    val = std::remove(temp.c_str());
    if (!val) {
        std::cout << "deleted " << (fileStart + ".bim") << '\n';
    }
    temp = fileStart + ".fam";
    val = std::remove(temp.c_str());
    if (!val) {
        std::cout << "deleted " << (fileStart + ".fam") << '\n';
    }

}

// writes fam file given a FamType object
void writeFamFileObject( const FamType &ft, const string &filePath)
{
    std::ofstream file(filePath);

    if (!file.is_open())
        perror("Error - file not able to open");
    for (auto &i : ft.ped)
    {
        file << (i->familyId + " " + i->id + " " + i->sire + " " + i->dam + " ") << i->gender << " " << i->phen << "\n";
    }
    file.close();
}

// Writes file, given a 2d vector of strings to define the pedigree
void writeFamFile(const string &filePath, const std::vector<std::vector<std::string>> &pedigree, const std::vector<int> &genders, const std::vector<int> &familyIds)
{
    std::ofstream file(filePath);

    if (!file.is_open())
        perror("Error - file not able to open");
    string famId = "0";
    string gender = "0";
    string phenotype = "-9";
    for (int i = 0; i < pedigree.size(); i++)
    {
        auto &an = pedigree[i];
        if (familyIds.size() != 0)
        {
            famId = std::to_string(familyIds[i]);
        }
        if (genders.size() != 0)
        {
            gender = std::to_string(genders[i]);
        }
        else
            file << (famId + " " + an[0] + " " + an[1] + " " + an[2]) << " " << gender << " " << phenotype << "\n";
    }
    file.close();
}

// Writes bim file given Bim object
void writeBimFile(const BimType bt, const std::string &filePath)
{
    std::ofstream file(filePath);

    if (!file.is_open())
        perror("Error - file not able to open");
    for (snp_ptr snps : bt.snps)
    {
        file << snps->chrom << '\t' << snps->name << '\t' << snps->basepair << '\t' << snps->number << '\t' << snps->refAllele << '\t' << snps->altAllele << '\n';
    }

    file.close();
}

/**
 * Appends a vector of snps in the format snpVector[snps, individual]
 * appends to both the bim and the bed binary files
 */
void appendLociToBedAndBimFiles(bedType &snpVector, const std::string filePath)
{
    int codes[4] = {2, 1, 0, 9};
    const int PLINKMULTIPLE = 4;
    long nAnimals = snpVector[0].size();
    //    set nAnimals to multiple of 4
    if (nAnimals % 4 != 0)
    {
        nAnimals = nAnimals + PLINKMULTIPLE / 2;
        nAnimals -= nAnimals % PLINKMULTIPLE;
    }
    const unsigned long size = (unsigned long)snpVector.size() * nAnimals * 2;

    BitHolder output{size};
    int count = 0;
    std::ofstream bimFile(filePath + ".bim", std::ios::out | std::ios::app);
    std::vector<int> tmpVec = {static_cast<int>(snpVector.size())};
    BimType bt = BimType(snpVector.size(), tmpVec);
    for (snp_ptr snps : bt.snps)
    {
        bimFile << snps->chrom << '\t' << snps->name << '\t' << snps->basepair << '\t' << snps->number << '\t' << snps->refAllele << '\t' << snps->altAllele << '\n';
    }
    bimFile.close();
    for (auto &snp : snpVector)
    {
        for (int g : snp)
        {
            if (g == codes[0])
            {
                output[count++] = 0;
                output[count++] = 0;
            }

            if (g == codes[3])
            {
                output[count++] = 1;
                output[count++] = 0;
            }
            if (g == codes[1])
            {
                output[count++] = 0;
                output[count++] = 1;
            }
            if (g == codes[2])
            {
                output[count++] = 1;
                output[count++] = 1;
            }
        }
    }
    // turn of sying to avoid pointless sying
    std::ios_base::sync_with_stdio(false);
    std::string path = filePath + ".bed";
    std::fstream file;
    if (!doesFileExist(path.c_str()))
    {
        file.open(path, std::ios::out | std::ios::binary);
        const char header[3] = {0x6c, 0x1b, 0x01};
        file.write((char *)header, 3);
    }
    else
    {
        file.open(path, std::ios_base::binary | std::ios_base::out | std::ios_base::app);
    }
    if (!file.is_open())
        perror("Error - file not found");

    file.write((char *)&output.array[0], output.array.size() * sizeof(unsigned char));
    file.close();
}

/**
 * writes a set of genotypes to a bed file in format genotypes[snps,individals]
 * 
 */
void writeBedFile(const bedType &genotypes, const std::string filePath)
{
    const char header[3] = {0x6c, 0x1b, 0x01};
    int codes[4] = {2, 1, 0, 9};

    const int PLINKMULTIPLE = 4;
    int nSnps = genotypes.size();
    if (nSnps == 0)
    {
        throw new NoSnpsException();
    }
    long nAnimals = genotypes[0].size();

    //        set nAnimals to multiple of 4
    if (nAnimals % 4 != 0)
    {
        nAnimals = nAnimals + PLINKMULTIPLE / 2;
        nAnimals -= nAnimals % PLINKMULTIPLE;
    }

    const unsigned long size = (unsigned long)nSnps * 2 * nAnimals;
    BitHolder output{size};
    size_t count = 0;
    for (auto &snp : genotypes)
    {
        for (int gPerAnimal : snp)
        {
            if (gPerAnimal == codes[0])
            {
                output[count++] = 0;
                output[count++] = 0;
            }

            if (gPerAnimal == codes[3])
            {
                output[count++] = 1;
                output[count++] = 0;
            }
            if (gPerAnimal == codes[1])
            {
                output[count++] = 0;
                output[count++] = 1;
            }
            if (gPerAnimal == codes[2])
            {
                output[count++] = 1;
                output[count++] = 1;
            }
        }
    }
    std::ios_base::sync_with_stdio(false);
    std::fstream file;
    
    file.open(filePath, std::ios::out | std::ios::binary);

    if (!file.is_open())
        perror("Error - file not found");
    file.write((char *)header, 3);
    file.write((char *)&output.array[0], output.array.size() * sizeof(unsigned char));
    file.close();
}

// function reads in a bim file to a bimtype object
BimType readInBimFile(const string fileName)
{

    BimType pt = BimType();
    std::string line;
    std::ifstream myfile(fileName);

    if (!myfile.is_open())
        perror("Error - file not found");
    //myfile.exceptions(std::ifstream::failbit);
    snp_ptr curSnp;
    int curChrom = -1;
    Chromosome *curChromPoint;
    while (std::getline(myfile, line))
    {
        boost::replace_all(line, "\t", " ");
        std::vector<string> lineVec = splitString(line, ' ');
        int lChrom = stoi(lineVec[0]);
        if (lChrom != curChrom)
        {
            if (curChrom != -1)
            {
                pt.chromosomes.push_back(std::make_shared<Chromosome>(*curChromPoint));
            }
            curChromPoint = new Chromosome();
            curChrom = lChrom;
        }
        curSnp = std::make_shared<Snp>(lineVec);
        curChromPoint->snps.push_back(curSnp);
        pt.snps.push_back(curSnp);
    }
    if (curChrom != -1)
    {
        auto sh = std::make_shared<Chromosome>(*curChromPoint);
        pt.chromosomes.push_back(sh);
    }

    myfile.close();
    return pt;
}

// reads in a fam file to a FamType Object
FamType readInFamFile(string fileName)
{
    std::ifstream myfile(fileName);
//myfile.exceptions(std::ifstream::failbit);
    string line;

    FamType ret = FamType();
    std::shared_ptr<FamObject> cur;
    if (!myfile.is_open())
        perror("Error - file not found");
    while (std::getline(myfile, line))
    {

        std::vector<string> lineVec = splitString(line, ' ');
        cur = std::make_shared<FamObject>();
        cur->familyId = lineVec[0];
        cur->id = lineVec[1];
        cur->sire = lineVec[2];
        cur->dam = lineVec[3];
        cur->gender = lineVec[4];
        cur->phen = lineVec[5];
        ret.ped.push_back(std::move(cur));
    }
    myfile.close();

    return ret;
}

/**
 * function reads a bed file into a 2d vector of form [snp,individual]
 * function needs the corresponding bimInfo and Famtype object from the corresponding files
 * 
 */
bedType readInBedFile(const string filePath, const int& nAnimals)
{
    const int HEADERSIZE = 3;
    const int BLOCKSIZE = 8;
    const char header[3] = {0x6c, 0x1b, 0x01};
    // constexpr std::array<int, 4> codes = {0x0, 0x1, 0x2, 0x9};
    constexpr std::array<int, 4> codes = {0x2, 0x1, 0x0, 0x9};

    std::fstream file;
    file.open(filePath, std::ios::in | std::ios::binary);

    if (!file.is_open())
        perror("Error - file not found");
    //file.exceptions(std::ifstream::failbit);
    char t[HEADERSIZE];
    std::vector<std::vector<genotypeIntType>> ret = {};

    try {
        file.read((char *) t, HEADERSIZE);

        for (int i = 0; i < HEADERSIZE; i++) {
            if (t[i] != header[i])
                throw new IncorrectHeaderException();
        }

        char c;
        std::bitset<BLOCKSIZE> bits;
        ret.emplace_back();

        int animCount = 0;
        while (file.get(c)) {
            for (int i = 0; i < BLOCKSIZE - 1; i = i + 2) //we read two bits in per value
            {
                animCount++;
                bool one = getBit(c, i);
                bool two = getBit(c, i + 1);

                if (!one and !two) {
                    ret.back().push_back(codes[0]);
                } else if (one && !two) {
                    ret.back().push_back(codes[3]);
                } else if (!one && two) {
                    ret.back().push_back(codes[1]);
                } else if (one && two) {
                    ret.back().push_back(codes[2]);
                }
                if (animCount == nAnimals) {
                    ret.emplace_back();
                    animCount = 0;
                }
            }
        }

        ret.pop_back();
    }
    catch (const std::exception& e) {
        throw BedReadException();
    }
    return ret;
}



PlinkHolder readPlink(const string& start) {

    FamType fam = readInFamFile(start + ".fam");

    BimType bim = readInBimFile(start+".bim");

    bedType bed = readInBedFile(start+".bed", fam.ped.size());


    return PlinkHolder(fam, bim, bed);

}


void writePlink(const string& start, const PlinkHolder& ph) {

    writeFamFileObject(ph.fam,start+".fam");
    writeBimFile(ph.bim, start+".bim");
    writeBedFile(ph.bed, start+".bed");

}




