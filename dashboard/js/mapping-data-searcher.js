  /**
   * managing the mapping data
   * @class MappingDataSearcher
   */
  function MappingDataSearcher() {}
  
// look for the country in a given array
MappingDataSearcher.search = function (nameKey, myArray){
    for (var i=0; i < myArray.length; i++) {

        if (myArray[i][0] === "Country") {
            // ignore that first row
        }
        else if (myArray[i][0] === nameKey) {
            console.log("Value found in mapping data.");
            myArray[i][1] += 1;
            return myArray;
        }           
    }

    console.log("Value not found in mapping data. Appending.");
    myArray.push([nameKey, 1]);
    return myArray;
}