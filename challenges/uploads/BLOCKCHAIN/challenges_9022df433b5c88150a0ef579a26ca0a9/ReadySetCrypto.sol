// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract Crypto{
    
    string private str = "0x63616c6c206d652063727970746f";
    string private temp = "0x6374627b3748335f4352593937305f4d314e33527d";
    
    function string_to_bytes(string memory s) public pure returns(bytes memory ){
        
        bytes memory b = bytes(s);
        return b;
    }
    
    function bytes_to_string(bytes memory b) public pure returns(string memory){
        
        string memory s = string(b);
        return s;
    }
}