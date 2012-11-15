--
-- Implement a function which finds the maximum of two values.
-- For example
-- max' 2 3 => 3
-- max' 5 4 => 5
--
max' :: (Ord a) => a -> a -> Bool


--
-- Find a function which finds the minimum of two values
-- For example
-- min' 2 3 => 2
-- min' 5 4 => 4
--
min' :: (Ord a) => a -> a -> Bool


--
-- Implement the logical function "and"
-- For example
-- and' True False => False
-- and' True True => True
--
and' :: Bool -> Bool -> Bool


--
-- Implement the logical function "or"
-- For example
-- or' False False => False
-- or' False True => True
--
or' :: Bool -> Bool -> Bool

--
-- Implement the logical function "not" 
-- For example
-- not' False => True
--
not' :: Bool -> Bool

--
-- Implement a function which adds two to any number it's given
-- For example
-- plusTwo 2 => 4
-- plusTwo 5 => 7
--
plusTwo :: (Num a) => a -> a

--
-- Implement a function which adds two to every number of a list
-- For example
-- plusTwoList [1,2,3] => [3,4,5]
-- plusTwoList [100] => [102]
--
plusTwoList :: (Num a) => [a] -> [a]
--
-- Given the functions 'odd' and 'even' below, prove that they always terminate
-- for any positive integer, and that they always terminate with the correct 
-- answer
--
odd' :: (Num a) => 
