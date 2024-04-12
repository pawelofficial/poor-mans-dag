this simple flask app allows you to print dag in ascii format via flask ( click raw to see the tree properly on gh )


*database1__schema1__table0*
└──>*database1__schema1__table1* ( DEPENDENCY )
    ├──>*database1__schema1__table2* ( DEPENDENCY )
    │   └──>*database1__schema1__table5* ( DEPENDENCY )
    │       └──>*database1__schema1__table9* ( DEPENDENCY )
    ├──>*database1__schema1__table3* ( DEPENDENCY )
    │   ├──>*database1__schema1__table4* ( DEPENDENCY )
    │   └──>*database1__schema1__table6* ( DEPENDENCY )
    ├──>*database1__schema1__table7* ( DEPENDENCY )
    └──>*database1__schema1__table8* ( DEPENDENCY )

database1__schema1__table4
*database1__schema1__table4*
└<──*database1__schema1__table3* ( DEPENDENCY )
    └<──*database1__schema1__table1* ( DEPENDENCY )
        └<──*database1__schema1__table0* ( DEPENDENCY )

database1__schema1__table6
*database1__schema1__table6*
└<──*database1__schema1__table3* ( DEPENDENCY )
    └<──*database1__schema1__table1* ( DEPENDENCY )
        └<──*database1__schema1__table0* ( DEPENDENCY )


![image](https://github.com/pawelofficial/my-sf-dag/assets/47770546/cbafc4fa-e8e9-4ceb-9dd1-1a5b76736ea7)


to do:
    - allow for config  
