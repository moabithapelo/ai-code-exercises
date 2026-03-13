// test.js - Comprehensive test suite for mergeSort
const { mergeSort } = require('./mergeSort');

function testMergeSort() {
    console.log("=== MERGE SORT TEST SUITE ===\n");
    
    let passedTests = 0;
    let totalTests = 0;
    
    function assertEqual(actual, expected, testName) {
        totalTests++;
        const actualStr = JSON.stringify(actual);
        const expectedStr = JSON.stringify(expected);
        
        if (actualStr === expectedStr) {
            console.log(`✅ PASS: ${testName}`);
            passedTests++;
        } else {
            console.log(`❌ FAIL: ${testName}`);
            console.log(`   Expected: ${expectedStr}`);
            console.log(`   Got:      ${actualStr}`);
        }
    }
    
    // Test 1: Empty array
    assertEqual(
        mergeSort([]),
        [],
        "Empty array"
    );
    
    // Test 2: Single element
    assertEqual(
        mergeSort([1]),
        [1],
        "Single element"
    );
    
    // Test 3: Two elements unsorted
    assertEqual(
        mergeSort([2, 1]),
        [1, 2],
        "Two elements unsorted"
    );
    
    // Test 4: Two elements sorted
    assertEqual(
        mergeSort([1, 2]),
        [1, 2],
        "Two elements sorted"
    );
    
    // Test 5: Multiple elements with duplicates
    assertEqual(
        mergeSort([3, 1, 4, 1, 5, 9, 2, 6]),
        [1, 1, 2, 3, 4, 5, 6, 9],
        "Multiple elements with duplicates"
    );
    
    // Test 6: Reverse sorted array
    assertEqual(
        mergeSort([5, 4, 3, 2, 1]),
        [1, 2, 3, 4, 5],
        "Reverse sorted"
    );
    
    // Test 7: Already sorted array
    assertEqual(
        mergeSort([1, 2, 3, 4, 5]),
        [1, 2, 3, 4, 5],
        "Already sorted"
    );
    
    // Test 8: All same values
    assertEqual(
        mergeSort([1, 1, 1, 1]),
        [1, 1, 1, 1],
        "All same values"
    );
    
    // Test 9: Negative numbers
    assertEqual(
        mergeSort([-3, -1, -2, 0, 2]),
        [-3, -2, -1, 0, 2],
        "Negative numbers"
    );
    
    // Test 10: Odd number of elements
    assertEqual(
        mergeSort([3, 1, 4, 2, 5]),
        [1, 2, 3, 4, 5],
        "Odd number of elements"
    );
    
    // Test 11: Large random array
    const randomArray = Array.from({ length: 100 }, () => 
        Math.floor(Math.random() * 100)
    );
    const sortedByMerge = mergeSort([...randomArray]);
    const sortedByNative = [...randomArray].sort((a, b) => a - b);
    assertEqual(
        sortedByMerge,
        sortedByNative,
        "Large random array (100 elements)"
    );
    
    // Test 12: Very large array (performance test)
    console.log("\n=== PERFORMANCE TEST ===");
    const largeArray = Array.from({ length: 10000 }, () => 
        Math.floor(Math.random() * 1000)
    );
    
    console.time("mergeSort");
    const largeSorted = mergeSort([...largeArray]);
    console.timeEnd("mergeSort");
    
    const largeNative = [...largeArray].sort((a, b) => a - b);
    const largeCorrect = JSON.stringify(largeSorted) === JSON.stringify(largeNative);
    console.log(`Large array correct: ${largeCorrect ? '✅' : '❌'}`);
    
    if (largeCorrect) passedTests++;
    totalTests++;
    
    // Test 13: Stability test
    console.log("\n=== STABILITY TEST ===");
    const stabilityArray = [
        { value: 3, id: 'a' },
        { value: 2, id: 'b' },
        { value: 3, id: 'c' },
        { value: 1, id: 'd' },
        { value: 2, id: 'e' }
    ];
    
    // For stability test, we need to compare by value but preserve order of equals
    const stableResult = mergeSort([...stabilityArray], (a, b) => a.value - b.value);
    console.log("Stable sort result (should preserve relative order):");
    console.log(stableResult.map(item => `${item.value}${item.id}`).join(', '));
    
    // Check if 'a' comes before 'c' (both value 3)
    const aIndex = stableResult.findIndex(item => item.id === 'a');
    const cIndex = stableResult.findIndex(item => item.id === 'c');
    const stable = aIndex < cIndex;
    console.log(`Stability preserved: ${stable ? '✅' : '❌'}`);
    
    if (stable) passedTests++;
    totalTests++;
    
    // Summary
    console.log(`\n=== SUMMARY ===`);
    console.log(`Passed: ${passedTests}/${totalTests} tests`);
    console.log(`Failed: ${totalTests - passedTests}/${totalTests} tests`);
    console.log(`Success rate: ${Math.round(passedTests / totalTests * 100)}%`);
}

// Run tests
testMergeSort();