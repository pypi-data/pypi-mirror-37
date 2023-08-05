#include "BitHolder.h"




BitHolder::BitHolder(std::size_t bits)
    : bits{bits},
      array{}
{
    // rounded-up division
    array.resize((bits + element_bits - 1) / element_bits);
}


    BitHolder::Bit BitHolder::operator[](std::size_t index) {
        if (index >= bits)
            throw std::out_of_range("Out of range");
        // return Bit(array[index / element_bits], 1u << (element_bits - (index % element_bits)) - 1);
        return Bit(array[index / element_bits], 1u << (index % element_bits));
}

size_t BitHolder::size() const {
    return this->bits;
}
