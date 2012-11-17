--
-- Implement a function which applies a function to every element of a list.
-- For example
-- map' (+2) [1,2,3] => [3,4,5]
-- map' (*5) [1,2,3] => [5,10,15]
-- map' undefined [] => []
-- 
map' :: (a -> b) -> [a] -> [b]


--
-- Implement a function to remove any elements of a list which do not meet a 
-- predicate
-- For example
-- filter' (>5) [1..10] => [6,7,8,9,10]
-- filter' (>100) [1..10] => []
--
filter' :: (a -> Bool) -> [a] -> [a]


--
-- Implement a function to take some number of items from the front of a list.
-- For example
-- take' 5 [1..10] => [1,2,3,4,5]
-- take' 100 [1..10] => [1,2,3,4,5,6,7,8,9,10]
--
take' :: Int -> [a] -> [a]


--
-- Implement a function to remove a number of items from the front of a list.
-- For example
-- drop' 5 [1..10] => [6,7,8,9,10]
-- drop' 100 [1..10] => []
--
drop' :: Int -> [a] -> [a]


--
-- Implement a function to find all prefixes of a list. Note that the order
-- the prefixes end up in the list does not matter.
-- For example:
-- prefixes [1,2,3] => [[1], [1,2], [1,2,3]]
-- 
prefixes :: [t] -> [[t]]


--
-- Implement a function to find all suffixes of a list. Note that the order 
-- the suffixes end up in the list does not matter.
-- For example:
-- suffixes [1,2,3] => [[1,2,3], [2,3], [3], []]
--
suffixes :: [t] -> [[t]]

--
-- Implement a function to find all sub-lists of a list. Note that the order
-- does not matter, however, the output should not contain any duplicates.
-- For example
-- subStrings "hello" = ["h","e","l","o", "he","el","ll",lo" .. "hello"]
--
subStrings :: [t] -> [[t]]

--
-- Treating a list as a mathematical set, implement a function to generate the
-- power set of a list. Not that it is the case that:
-- 
-- * All elements of the powerset are unique
-- * The size of the powerset is 2^n where n is the size of the input.
--
-- For example
-- powerSet [1,2,3] => [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]
-- length $ powerSet [1,2,3] => 8 
--
