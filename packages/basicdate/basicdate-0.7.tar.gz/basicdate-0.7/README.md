# Basicdate

Basicdate is a simple set of Python classes for simple date manipulation.

## Why another date util?

I just needed something quick for parsing dates in short set of predermined formats:

- YYYYMMDD
- YYYY-MM-DD
- DD-MM-YYYY
- DD/MM/YYYY

and needed something that could be convertible to a json type:

    {
       "_type": "BasicDate",
       "value": "YYYYMMDD"
    }
 
 Provided BasicDateEncoder and BasicDateDecoder classes can be used in json conversions as follows:
 
    json.loads('{"_type": "BasicDate", "value": "20180117"}', cls=BasicDateDecoder)

will return:
    
    BasicDate('17/01/2018')
 
and

    json.dumps(BasicDate('17/01/2018'), cls=BasicDateEncoder)
 
will return:
    
    '{"_type": "BasicDate", "value": "20180117"}'

BasicDate supports also simple arithmetic:
    
    BasicDate('17/01/2018') + 1 == BasicDate('18/01/2018')
    BasicDate('19/01/2018') - 2 == BasicDate('17/01/2018')

and comparisons:

    BasicDate('17/01/2018') < BasicDate('18/01/2018')
    
## What's particular?

The BasicDate has been implemented to support object identity.

So the following test is valid:

    a, b, c = BasicDate('17/01/2018'), BasicDate('17/01/2018'), BasicDate('18/01/2018')
    assert a == b
    assert a != c
    assert type(a) == type(b) == type(c)
    assert a is b
    assert a is not c
    assert a == c - 1
