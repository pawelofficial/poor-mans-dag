this simple flask app allows you to print dag in ascii format via flask 

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