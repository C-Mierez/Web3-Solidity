// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {

    /* Types
    uint256 favouriteNumber = 5;
    bool favouriteBool = true;
    string favouriteString = "String";
    int256 favouriteInt = -40;
    address favouriteAddress = 0xD8CBa55a6c304543c03f54125C651Eb5491a15a3;
    bytes32 favouriteBytes = "cat";
    */

    struct Person {
        string name;
        uint256 number;
    }

    uint256 public myNumber;
    Person[] public people;
    
    mapping(string => uint256) public nameToNumber;
    
    function store(uint256 _myNumber) public {
        myNumber =_myNumber;
    }

    // We can use the keywords (view, pure) for functions that don't require gas (Reading)
    function retrieve() public view returns(uint256){
        return myNumber;
    }

    // Keyword pure is used for functions that perform some kind of computation that is NOT saved
    function compute(uint256 number) public pure returns(uint256){
        return number + 10;
    }

    function addPerson(string memory _name, uint256 _number) public {
        people.push(Person({name: _name, number: _number}));
        nameToNumber[_name] = _number;
    }
}