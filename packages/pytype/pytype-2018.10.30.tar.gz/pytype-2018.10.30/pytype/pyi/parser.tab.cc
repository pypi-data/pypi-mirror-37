// A Bison parser, made by GNU Bison 3.0.4.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// Take the name prefix into account.
#define yylex   pytypelex

// First part of user declarations.

#line 39 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:404

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

#include "parser.tab.hh"

// User implementation prologue.

#line 53 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:412
// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:413

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 81 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:413


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (/*CONSTCOND*/ false)
# endif


// Suppress unused-variable warnings by "using" E.
#define YYUSE(E) ((void) (E))

// Enable debugging if requested.
#if YYDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << std::endl;                  \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yystack_print_ ();                \
  } while (false)

#else // !YYDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YYUSE(Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void>(0)
# define YY_STACK_PRINT()                static_cast<void>(0)

#endif // !YYDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:479
namespace pytype {
#line 167 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:479

  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr = "";
        char const *yyp = yystr;

        for (;;)
          switch (*++yyp)
            {
            case '\'':
            case ',':
              goto do_not_strip_quotes;

            case '\\':
              if (*++yyp != '\\')
                goto do_not_strip_quotes;
              // Fall through.
            default:
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }


  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
    :
#if YYDEBUG
      yydebug_ (false),
      yycdebug_ (&std::cerr),
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}


  /*---------------.
  | Symbol types.  |
  `---------------*/

  inline
  parser::syntax_error::syntax_error (const location_type& l, const std::string& m)
    : std::runtime_error (m)
    , location (l)
  {}

  // basic_symbol.
  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol ()
    : value ()
  {}

  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& other)
    : Base (other)
    , value ()
    , location (other.location)
  {
    value = other.value;
  }


  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, const semantic_type& v, const location_type& l)
    : Base (t)
    , value (v)
    , location (l)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, const location_type& l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  inline
  parser::basic_symbol<Base>::~basic_symbol ()
  {
    clear ();
  }

  template <typename Base>
  inline
  void
  parser::basic_symbol<Base>::clear ()
  {
    Base::clear ();
  }

  template <typename Base>
  inline
  bool
  parser::basic_symbol<Base>::empty () const
  {
    return Base::type_get () == empty_symbol;
  }

  template <typename Base>
  inline
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move(s);
    value = s.value;
    location = s.location;
  }

  // by_type.
  inline
  parser::by_type::by_type ()
    : type (empty_symbol)
  {}

  inline
  parser::by_type::by_type (const by_type& other)
    : type (other.type)
  {}

  inline
  parser::by_type::by_type (token_type t)
    : type (yytranslate_ (t))
  {}

  inline
  void
  parser::by_type::clear ()
  {
    type = empty_symbol;
  }

  inline
  void
  parser::by_type::move (by_type& that)
  {
    type = that.type;
    that.clear ();
  }

  inline
  int
  parser::by_type::type_get () const
  {
    return type;
  }


  // by_state.
  inline
  parser::by_state::by_state ()
    : state (empty_state)
  {}

  inline
  parser::by_state::by_state (const by_state& other)
    : state (other.state)
  {}

  inline
  void
  parser::by_state::clear ()
  {
    state = empty_state;
  }

  inline
  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  inline
  parser::by_state::by_state (state_type s)
    : state (s)
  {}

  inline
  parser::symbol_number_type
  parser::by_state::type_get () const
  {
    if (state == empty_state)
      return empty_symbol;
    else
      return yystos_[state];
  }

  inline
  parser::stack_symbol_type::stack_symbol_type ()
  {}


  inline
  parser::stack_symbol_type::stack_symbol_type (state_type s, symbol_type& that)
    : super_type (s, that.location)
  {
    value = that.value;
    // that is emptied.
    that.type = empty_symbol;
  }

  inline
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (const stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    return *this;
  }


  template <typename Base>
  inline
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.type_get ())
    {
            case 3: // NAME

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 421 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 4: // NUMBER

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 5: // LEXERROR

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 435 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 47: // start

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 442 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 48: // unit

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 449 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 49: // alldefs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 456 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 51: // classdef

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 463 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 52: // class_name

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 53: // parents

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 477 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 54: // parent_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 484 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 55: // parent

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 491 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 56: // maybe_class_funcs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 498 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 57: // class_funcs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 505 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 58: // funcdefs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 512 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 59: // if_stmt

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 519 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 60: // if_and_elifs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 526 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 61: // class_if_stmt

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 533 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 62: // class_if_and_elifs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 540 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 63: // if_cond

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 547 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 64: // elif_cond

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 554 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 65: // else_cond

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 561 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 66: // condition

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 568 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 67: // version_tuple

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 575 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 68: // condition_op

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.str)); }
#line 582 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 69: // constantdef

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 589 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 70: // importdef

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 71: // import_items

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 603 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 72: // import_item

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 610 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 73: // import_name

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 617 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 74: // from_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 624 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 75: // from_items

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 631 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 76: // from_item

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 638 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 77: // alias_or_constant

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 645 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 78: // typevardef

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 652 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 79: // typevar_args

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 659 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 80: // typevar_kwargs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 666 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 81: // typevar_kwarg

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 673 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 82: // funcdef

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 83: // decorators

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 687 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 84: // decorator

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 694 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 85: // params

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 701 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 86: // param_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 708 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 87: // param

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 715 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 88: // param_type

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 722 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 89: // param_default

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 729 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 90: // param_star_name

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 736 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 91: // return

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 743 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 93: // maybe_body

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 750 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 95: // body

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 757 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 96: // body_stmt

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 764 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 97: // type_parameters

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 771 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 98: // type_parameter

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 778 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 99: // type

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 785 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 100: // named_tuple_fields

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 792 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 101: // named_tuple_field_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 799 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 102: // named_tuple_field

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 806 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 104: // maybe_type_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 813 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 105: // type_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 106: // type_tuple_elements

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 827 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 107: // type_tuple_literal

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 834 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 108: // dotted_name

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 841 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 109: // getitem_key

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 848 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 110: // maybe_number

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 855 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;


      default:
        break;
    }
  }

#if YYDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo,
                                     const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YYUSE (yyoutput);
    symbol_number_type yytype = yysym.type_get ();
    // Avoid a (spurious) G++ 4.8 warning about "array subscript is
    // below array bounds".
    if (yysym.empty ())
      std::abort ();
    yyo << (yytype < yyntokens_ ? "token" : "nterm")
        << ' ' << yytname_[yytype] << " ("
        << yysym.location << ": ";
    YYUSE (yytype);
    yyo << ')';
  }
#endif

  inline
  void
  parser::yypush_ (const char* m, state_type s, symbol_type& sym)
  {
    stack_symbol_type t (s, sym);
    yypush_ (m, t);
  }

  inline
  void
  parser::yypush_ (const char* m, stack_symbol_type& s)
  {
    if (m)
      YY_SYMBOL_PRINT (m, s);
    yystack_.push (s);
  }

  inline
  void
  parser::yypop_ (unsigned int n)
  {
    yystack_.pop (n);
  }

#if YYDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // YYDEBUG

  inline parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - yyntokens_] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - yyntokens_];
  }

  inline bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  inline bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::parse ()
  {
    // State.
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

    // FIXME: This shoud be completely indented.  It is not yet to
    // avoid gratuitous conflicts when merging into the master branch.
    try
      {
    YYCDEBUG << "Starting parse" << std::endl;


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, yyla);

    // A new symbol was pushed on the stack.
  yynewstate:
    YYCDEBUG << "Entering state " << yystack_[0].state << std::endl;

    // Accept?
    if (yystack_[0].state == yyfinal_)
      goto yyacceptlab;

    goto yybackup;

    // Backup.
  yybackup:

    // Try to take a decision without lookahead.
    yyn = yypact_[yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token: ";
        try
          {
            yyla.type = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
        catch (const syntax_error& yyexc)
          {
            error (yyexc);
            goto yyerrlab1;
          }
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.type_get ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.type_get ())
      goto yydefault;

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", yyn, yyla);
    goto yynewstate;

  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;

  /*-----------------------------.
  | yyreduce -- Do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_(yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Compute the default @$.
      {
        slice<stack_symbol_type, stack_type> slice (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, slice, yylen);
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
      try
        {
          switch (yyn)
            {
  case 2:
#line 132 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1094 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 3:
#line 133 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1100 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 5:
#line 141 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1106 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 6:
#line 142 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1112 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 7:
#line 143 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1118 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 8:
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1129 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 9:
#line 150 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1135 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 10:
#line 151 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1141 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 11:
#line 152 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1151 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 12:
#line 157 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1157 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 15:
#line 168 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNN)", (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1166 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 16:
#line 175 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1179 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 17:
#line 186 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1185 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 18:
#line 187 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1191 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 19:
#line 188 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1197 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 20:
#line 192 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1203 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 21:
#line 193 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1209 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 22:
#line 197 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1215 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 23:
#line 198 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1221 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 24:
#line 202 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1227 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 25:
#line 203 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1233 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 26:
#line 204 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1239 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 27:
#line 208 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1245 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 29:
#line 213 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1251 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 30:
#line 214 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1261 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 31:
#line 219 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1267 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 32:
#line 220 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1277 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 33:
#line 225 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1283 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 34:
#line 226 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1289 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 35:
#line 231 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1297 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 37:
#line 239 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1305 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 38:
#line 243 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1313 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 39:
#line 262 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1321 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 41:
#line 270 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1329 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 42:
#line 274 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1337 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 43:
#line 286 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1343 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 44:
#line 290 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1349 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 45:
#line 294 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1355 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 46:
#line 298 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1363 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 47:
#line 301 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1371 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 48:
#line 304 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1379 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 49:
#line 307 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1387 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 50:
#line 310 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1393 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 51:
#line 311 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1399 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 52:
#line 312 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1405 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 53:
#line 317 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1411 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 54:
#line 318 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1417 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 55:
#line 319 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1425 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 56:
#line 325 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "<"; }
#line 1431 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 57:
#line 326 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = ">"; }
#line 1437 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 58:
#line 327 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "<="; }
#line 1443 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 59:
#line 328 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = ">="; }
#line 1449 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 60:
#line 329 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "=="; }
#line 1455 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 61:
#line 330 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "!="; }
#line 1461 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 62:
#line 334 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 63:
#line 338 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kByteString));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1479 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 64:
#line 342 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kUnicodeString));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1488 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 65:
#line 346 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1497 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 66:
#line 350 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1506 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 67:
#line 354 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1515 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 68:
#line 358 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1524 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 69:
#line 362 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1533 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 70:
#line 369 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1542 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 71:
#line 373 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1551 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 72:
#line 377 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1562 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 73:
#line 383 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Special-case "from .. import" and pass in a __PARENT__ token that
      // the Python parser code will rewrite to the parent package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PARENT__", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1573 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 74:
#line 392 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1579 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 75:
#line 393 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1585 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 77:
#line 397 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1591 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 79:
#line 403 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1600 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 81:
#line 411 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1606 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 82:
#line 412 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1612 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 83:
#line 416 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1618 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 84:
#line 417 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1624 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 86:
#line 422 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
 (yylhs.value.obj) = PyString_FromString("NamedTuple");
 }
#line 1632 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 87:
#line 425 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
 (yylhs.value.obj) = PyString_FromString("TypeVar");
 }
#line 1640 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 88:
#line 428 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
 (yylhs.value.obj) = PyString_FromString("*");
 }
#line 1648 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 89:
#line 431 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1654 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 90:
#line 435 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1660 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 91:
#line 439 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1669 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 92:
#line 446 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1675 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 93:
#line 447 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1681 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 94:
#line 448 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1687 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 95:
#line 449 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1693 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 96:
#line 453 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1699 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 97:
#line 454 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1705 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 98:
#line 458 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1711 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 99:
#line 462 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NNNNN)", (yystack_[7].value.obj), (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      //
      // TODO(dbaum): Consider making this smarter and only ignoring decorators
      // when they are empty.  Making decorators non-nullable and having two
      // productions for funcdef would be a reasonable solution.
      yylhs.location.begin = yystack_[6].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1730 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 100:
#line 479 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1736 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 101:
#line 480 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1742 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 102:
#line 484 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1748 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 103:
#line 488 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1754 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 104:
#line 489 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1760 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 105:
#line 501 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1766 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 106:
#line 502 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1772 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 107:
#line 506 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1778 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 108:
#line 507 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1784 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 109:
#line 508 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1790 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 110:
#line 509 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1796 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 111:
#line 513 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1802 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 112:
#line 514 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1808 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 113:
#line 518 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1814 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 114:
#line 519 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 115:
#line 520 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1826 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 116:
#line 521 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1832 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 117:
#line 525 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1838 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 118:
#line 526 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1844 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 119:
#line 530 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1850 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 120:
#line 531 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 1856 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 121:
#line 535 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_DecRef((yystack_[0].value.obj)); }
#line 1862 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 122:
#line 539 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1868 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 123:
#line 540 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1874 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 124:
#line 541 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1880 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 132:
#line 555 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1886 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 133:
#line 556 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1892 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 134:
#line 560 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1898 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 135:
#line 561 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1904 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 136:
#line 562 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1910 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 137:
#line 566 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1916 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 138:
#line 567 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1922 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 139:
#line 571 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1928 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 140:
#line 572 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1934 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 141:
#line 576 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1943 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 142:
#line 580 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1952 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 143:
#line 584 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // This rule is needed for Callable[[...], ...]
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1962 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 144:
#line 589 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1971 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 145:
#line 593 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1977 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 146:
#line 594 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1983 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 147:
#line 595 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1989 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 148:
#line 596 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 1995 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 149:
#line 597 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 2001 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 150:
#line 601 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2007 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 151:
#line 602 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 2013 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 152:
#line 606 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2019 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 153:
#line 607 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2025 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 154:
#line 611 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2031 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 157:
#line 620 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2037 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 158:
#line 621 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 2043 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 159:
#line 625 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2049 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 160:
#line 626 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2055 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 161:
#line 633 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2061 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 162:
#line 634 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2067 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 163:
#line 643 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2076 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 164:
#line 648 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2085 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 165:
#line 654 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2094 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 166:
#line 661 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2100 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 167:
#line 662 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2116 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 168:
#line 676 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2122 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 169:
#line 677 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2132 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 170:
#line 682 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2142 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 171:
#line 690 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2148 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 172:
#line 691 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = NULL; }
#line 2154 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;


#line 2158 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
            default:
              break;
            }
        }
      catch (const syntax_error& yyexc)
        {
          error (yyexc);
          YYERROR;
        }
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;
      YY_STACK_PRINT ();

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, yylhs);
    }
    goto yynewstate;

  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        error (yyla.location, yysyntax_error_ (yystack_[0].state, yyla));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.type_get () == yyeof_)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:

    /* Pacify compilers like GCC when the user code never invokes
       YYERROR and the label yyerrorlab therefore never appears in user
       code.  */
    if (false)
      goto yyerrorlab;
    yyerror_range[1].location = yystack_[yylen - 1].location;
    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    goto yyerrlab1;

  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    {
      stack_symbol_type error_token;
      for (;;)
        {
          yyn = yypact_[yystack_[0].state];
          if (!yy_pact_value_is_default_ (yyn))
            {
              yyn += yyterror_;
              if (0 <= yyn && yyn <= yylast_ && yycheck_[yyn] == yyterror_)
                {
                  yyn = yytable_[yyn];
                  if (0 < yyn)
                    break;
                }
            }

          // Pop the current state because it cannot handle the error token.
          if (yystack_.size () == 1)
            YYABORT;

          yyerror_range[1].location = yystack_[0].location;
          yy_destroy_ ("Error: popping", yystack_[0]);
          yypop_ ();
          YY_STACK_PRINT ();
        }

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = yyn;
      yypush_ ("Shifting", error_token);
    }
    goto yynewstate;

    // Accept.
  yyacceptlab:
    yyresult = 0;
    goto yyreturn;

    // Abort.
  yyabortlab:
    yyresult = 1;
    goto yyreturn;

  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack"
                 << std::endl;
        // Do not try to display the values of the reclaimed symbols,
        // as their printer might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what());
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (state_type yystate, const symbol_type& yyla) const
  {
    // Number of reported tokens (one for the "unexpected", one per
    // "expected").
    size_t yycount = 0;
    // Its maximum.
    enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
    // Arguments of yyformat.
    char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];

    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state
         merging (from LALR or IELR) and default reductions corrupt the
         expected token list.  However, the list is correct for
         canonical LR with one exception: it will still contain any
         token that will not be accepted due to an error action in a
         later state.
    */
    if (!yyla.empty ())
      {
        int yytoken = yyla.type_get ();
        yyarg[yycount++] = yytname_[yytoken];
        int yyn = yypact_[yystate];
        if (!yy_pact_value_is_default_ (yyn))
          {
            /* Start YYX at -YYN if negative to avoid negative indexes in
               YYCHECK.  In other words, skip the first -YYN actions for
               this state because they are default actions.  */
            int yyxbegin = yyn < 0 ? -yyn : 0;
            // Stay within bounds of both yycheck and yytname.
            int yychecklim = yylast_ - yyn + 1;
            int yyxend = yychecklim < yyntokens_ ? yychecklim : yyntokens_;
            for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
              if (yycheck_[yyx + yyn] == yyx && yyx != yyterror_
                  && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
                {
                  if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                    {
                      yycount = 1;
                      break;
                    }
                  else
                    yyarg[yycount++] = yytname_[yyx];
                }
          }
      }

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
        YYCASE_(0, YY_("syntax error"));
        YYCASE_(1, YY_("syntax error, unexpected %s"));
        YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    size_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += yytnamerr_ (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short int parser::yypact_ninf_ = -220;

  const short int parser::yytable_ninf_ = -172;

  const short int
  parser::yypact_[] =
  {
     -13,  -220,    22,    90,   315,   123,  -220,  -220,   -19,   133,
     110,   175,    40,  -220,  -220,   308,   157,  -220,  -220,  -220,
    -220,  -220,    28,  -220,     2,   131,  -220,   154,  -220,   110,
     323,   266,   169,  -220,    -1,    63,   231,   225,  -220,   110,
     238,   252,   269,   284,   175,  -220,  -220,   259,     2,     2,
    -220,   173,   197,  -220,   279,   290,  -220,  -220,     2,   205,
    -220,    14,   298,   262,   110,   110,  -220,  -220,  -220,  -220,
     332,  -220,  -220,   336,   111,   175,   343,    10,   112,  -220,
      10,   323,   324,   325,  -220,   319,   126,   351,   264,   331,
     316,   320,     2,     2,   354,   337,  -220,  -220,    20,   355,
       2,    52,   326,  -220,   327,  -220,   309,  -220,   331,   330,
    -220,   349,  -220,   333,   328,   335,  -220,  -220,   359,  -220,
    -220,  -220,   353,  -220,  -220,    59,  -220,  -220,   329,  -220,
      10,    43,  -220,  -220,  -220,   218,   117,  -220,   334,  -220,
    -220,     2,   360,  -220,  -220,   330,  -220,   107,  -220,   331,
     338,    97,   103,     2,   340,     2,  -220,   161,   310,   286,
     367,   341,   370,   312,    59,  -220,   228,   234,  -220,   345,
    -220,     7,   344,   346,  -220,   345,   342,   331,  -220,    20,
    -220,   164,   348,  -220,  -220,   331,   331,  -220,   331,  -220,
    -220,  -220,   273,  -220,   330,   138,  -220,   352,   162,  -220,
    -220,   172,  -220,  -220,  -220,     2,   339,  -220,   378,   363,
     166,  -220,  -220,   230,   356,  -220,   350,   357,  -220,   358,
    -220,   148,   361,   244,  -220,  -220,  -220,  -220,   367,   314,
    -220,  -220,   331,   278,  -220,  -220,     2,   362,   117,   383,
    -220,   364,  -220,  -220,     2,   385,   164,   368,  -220,   220,
    -220,  -220,   308,   365,  -220,  -220,  -220,  -220,  -220,   386,
    -220,  -220,  -220,   331,   292,  -220,  -220,  -220,   366,   369,
     371,   331,   350,  -220,   357,  -220,   155,   372,   373,   374,
     376,   201,   311,   330,     2,  -220,  -220,   377,   380,  -220,
    -220,   375,     2,   381,   191,  -220,   387,   281,  -220,  -220,
     215,  -220,  -220,   249,     2,   267,  -220,  -220,  -220,  -220,
     208,   388,  -220,   379,   255,   260,  -220,   331,   382,  -220,
    -220,  -220,  -220,  -220,  -220
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   101,     0,     1,     2,     0,     0,
       0,     0,     0,     9,    11,    36,     0,     5,     7,     8,
      10,     6,     0,     3,     0,     0,    16,    19,   166,     0,
      43,     0,    70,    75,    76,     0,     0,    78,    45,     0,
       0,     0,     0,     0,     0,   100,   149,     0,     0,   158,
     148,    14,   141,    62,     0,    66,    63,    64,     0,    90,
      65,     0,     0,     0,     0,     0,    60,    61,    58,    59,
     172,    56,    57,     0,     0,     0,     0,     0,     0,    79,
       0,    44,     0,     0,    12,     0,    14,     0,     0,   160,
       0,   157,     0,     0,     0,     0,    68,    13,     0,     0,
       0,     0,   156,   165,   166,    18,     0,    21,    22,    14,
      52,    51,    50,   168,     0,     0,   167,    46,     0,    47,
      74,    77,    85,    86,    87,     0,    88,    72,    80,    84,
       0,     0,    71,    12,    12,   101,   104,   102,     0,   145,
     143,     0,   147,   146,   121,    14,   140,     0,   138,   139,
      92,    14,     0,   155,     0,     0,    17,     0,     0,     0,
     172,     0,     0,     0,     0,    73,   101,   101,    37,   112,
     110,   108,     0,   156,   106,   112,     0,   159,    69,     0,
     142,     0,     0,    67,   164,   162,   161,   163,    23,    20,
     173,   174,    34,    15,    14,     0,   171,   169,     0,    89,
      81,     0,    83,    38,    35,     0,   116,   117,     0,   120,
      14,   103,   109,     0,     0,   137,   166,    94,    97,    93,
      91,    34,     0,   101,    27,    24,    48,    49,   172,     0,
      53,    82,   111,     0,   107,   118,     0,   131,     0,     0,
     151,   156,   153,   144,     0,     0,     0,     0,    25,     0,
      33,    32,    40,     0,    29,    30,    31,   170,    54,     0,
     113,   114,   115,   119,     0,    99,   124,   105,     0,   155,
       0,    98,     0,    96,    95,    26,     0,     0,     0,     0,
       0,     0,     0,   125,     0,   152,   150,     0,     0,    34,
      55,     0,     0,     0,     0,   133,     0,     0,   127,   126,
     156,    34,    34,   101,     0,   135,   130,   123,   132,   129,
       0,     0,   155,     0,   101,   101,    41,   134,     0,   122,
     128,   154,    42,    39,   136
  };

  const short int
  parser::yypgoto_[] =
  {
    -220,  -220,   391,   -77,   -78,  -219,  -220,  -220,  -220,   240,
    -220,   178,    39,  -220,  -220,  -220,  -220,  -217,   156,   167,
      54,   223,   254,  -214,  -220,  -220,   347,   408,   -69,   296,
     -89,  -211,  -220,  -220,   177,   179,  -204,  -220,  -220,  -220,
    -220,   187,   251,  -220,  -220,  -220,  -112,  -220,  -220,   130,
     -81,  -220,   250,   -24,  -220,  -220,   159,  -170,  -220,   253,
    -220,  -220,    16,  -220,  -158,  -157
  };

  const short int
  parser::yydefgoto_[] =
  {
      -1,     2,     3,     4,    96,    13,    27,    62,   106,   107,
     193,   222,   223,    14,    15,   251,   252,    16,    40,    41,
      30,   119,    74,    17,    18,    32,    33,    79,   127,   128,
     129,    19,    20,   182,   217,   218,    21,    22,    45,   172,
     173,   174,   206,   234,   175,   237,    97,   265,   266,   294,
     295,   147,   148,    59,   214,   241,   242,   154,    90,    91,
     102,    60,    52,   114,   115,   224
  };

  const short int
  parser::yytable_[] =
  {
      51,   194,   197,   211,   250,    28,   253,   135,   137,   254,
     207,   132,   255,   122,    24,    76,     1,   104,    25,   256,
      46,    47,     6,    28,    88,    89,    31,    34,    37,   123,
     124,   158,    46,    47,   101,    43,    48,   108,    46,    47,
      49,    73,   146,    28,   125,    31,    28,    50,    48,   105,
     208,    37,    49,   126,    48,    31,   166,   167,    49,    50,
      86,   165,   122,    92,    93,    50,    28,   178,   142,   143,
     257,   270,    44,   183,   149,   202,   151,    77,   123,   124,
      31,    31,    35,    63,   250,   131,   253,   139,   152,   254,
       7,    34,   255,    81,    37,   250,   250,   253,   253,   256,
     254,   254,   126,   255,   255,    78,    28,   283,    92,    93,
     256,   256,   202,    28,   117,    28,   225,   177,   111,   112,
     169,    46,    47,    23,   296,   298,   130,    94,   185,   186,
     313,   188,   238,   108,    28,    53,    26,    48,   184,   170,
     311,    49,   226,   179,    29,   118,   180,    37,    50,    46,
      47,    54,   282,    55,   131,   149,    94,    89,    28,    53,
     171,   190,    56,    57,   104,    58,   229,   216,    73,    49,
     191,   299,   118,    46,    47,   122,    50,    55,    28,    46,
      47,   232,    46,    47,    92,    93,    56,    57,    61,    58,
      42,   123,   124,    49,   291,    48,    94,   230,    48,    49,
      50,  -155,    49,    94,   291,    75,    50,   231,   292,    50,
      95,   291,   263,   308,   190,   126,    92,    93,   292,   307,
     271,     8,   177,   191,     9,   292,    92,    93,    10,   308,
     293,     8,    11,    12,     9,    98,   319,     8,    10,    73,
       9,   103,    11,    12,    10,    80,   168,   249,    11,    12,
       9,   312,   249,    24,    10,     9,   203,   276,   249,    10,
     300,     9,   204,   249,   239,    10,     9,    73,   305,   240,
      10,    82,   -28,    64,    65,    92,    93,   316,    92,    93,
     317,   260,   261,   322,   291,    83,   190,    85,   323,    66,
      67,    68,    69,    87,   190,   191,    84,   110,   292,   139,
     262,   318,   221,   191,    70,   190,    71,    72,    73,    66,
      67,    68,    69,    99,   191,    -4,    38,    39,     8,   281,
     100,     9,    94,   190,   190,    10,    71,    72,   303,    11,
      12,   109,   191,   191,    64,    65,   113,   192,   297,   116,
     314,   315,    92,    93,   156,   157,   121,   200,   201,   258,
     259,   133,   134,   136,   138,   140,   141,   144,   150,   145,
      94,    65,   153,   161,   155,   164,  -171,   159,   160,   162,
     176,   196,    93,   199,   181,   187,   233,   198,   205,   209,
     213,   235,   210,   220,   236,   228,   268,   244,   272,   248,
     280,   243,     5,   245,   246,   264,   275,   189,   279,   247,
     269,   289,   284,   239,   301,   287,   288,   302,   277,   306,
     286,   290,   304,   195,   321,   309,   320,   324,   227,   278,
      36,   163,   120,   274,   273,   267,   212,   310,   285,   215,
       0,     0,     0,     0,   219
  };

  const short int
  parser::yycheck_[] =
  {
      24,   158,   160,   173,   223,     3,   223,    84,    86,   223,
       3,    80,   223,     3,    33,    16,    29,     3,    37,   223,
      18,    19,     0,     3,    48,    49,    10,    11,    12,    19,
      20,   109,    18,    19,    58,     7,    34,    61,    18,    19,
      38,    42,    22,     3,    34,    29,     3,    45,    34,    35,
      43,    35,    38,    43,    34,    39,   133,   134,    38,    45,
      44,   130,     3,    11,    12,    45,     3,   145,    92,    93,
     228,   241,    44,   151,    98,   164,   100,    14,    19,    20,
      64,    65,    42,    29,   303,    42,   303,    35,    36,   303,
       0,    75,   303,    39,    78,   314,   315,   314,   315,   303,
     314,   315,    43,   314,   315,    42,     3,   264,    11,    12,
     314,   315,   201,     3,     3,     3,   194,   141,    64,    65,
       3,    18,    19,     0,   281,   282,    14,    30,   152,   153,
     300,   155,   210,   157,     3,     4,     3,    34,    35,    22,
     297,    38,     4,    36,    34,    34,    39,   131,    45,    18,
      19,    20,   264,    22,    42,   179,    30,   181,     3,     4,
      43,    13,    31,    32,     3,    34,     4,     3,    42,    38,
      22,   283,    34,    18,    19,     3,    45,    22,     3,    18,
      19,   205,    18,    19,    11,    12,    31,    32,    34,    34,
      33,    19,    20,    38,     3,    34,    30,    35,    34,    38,
      45,    35,    38,    30,     3,    36,    45,    35,    17,    45,
      37,     3,   236,   294,    13,    43,    11,    12,    17,    28,
     244,     3,   246,    22,     6,    17,    11,    12,    10,   310,
      29,     3,    14,    15,     6,    38,    28,     3,    10,    42,
       6,    36,    14,    15,    10,    14,    28,     3,    14,    15,
       6,    36,     3,    33,    10,     6,    28,    37,     3,    10,
     284,     6,    28,     3,    34,    10,     6,    42,   292,    39,
      10,    33,    28,    11,    12,    11,    12,    28,    11,    12,
     304,     3,     4,    28,     3,    33,    13,     3,    28,    23,
      24,    25,    26,    34,    13,    22,    27,    35,    17,    35,
      22,    34,    29,    22,    38,    13,    40,    41,    42,    23,
      24,    25,    26,    34,    22,     0,     8,     9,     3,    27,
      30,     6,    30,    13,    13,    10,    40,    41,   289,    14,
      15,    33,    22,    22,    11,    12,     4,    27,    27,     3,
     301,   302,    11,    12,    35,    36,     3,    35,    36,    35,
      36,    27,    27,    34,     3,    39,    36,     3,     3,    22,
      30,    12,    36,     4,    37,    36,    33,    39,    33,    16,
      36,     4,    12,     3,    36,    35,    37,    36,    33,    35,
      38,     3,    36,    35,    21,    33,     3,    37,     3,    28,
       4,    35,     1,    36,    36,    33,    28,   157,    33,   221,
      36,    27,    36,    34,    27,    33,    33,    27,   252,    28,
      39,    35,    37,   159,    35,    28,    28,    35,   195,   252,
      12,   125,    75,   246,   245,   238,   175,   297,   269,   179,
      -1,    -1,    -1,    -1,   181
  };

  const unsigned char
  parser::yystos_[] =
  {
       0,    29,    47,    48,    49,    48,     0,     0,     3,     6,
      10,    14,    15,    51,    59,    60,    63,    69,    70,    77,
      78,    82,    83,     0,    33,    37,     3,    52,     3,    34,
      66,   108,    71,    72,   108,    42,    73,   108,     8,     9,
      64,    65,    33,     7,    44,    84,    18,    19,    34,    38,
      45,    99,   108,     4,    20,    22,    31,    32,    34,    99,
     107,    34,    53,    66,    11,    12,    23,    24,    25,    26,
      38,    40,    41,    42,    68,    36,    16,    14,    42,    73,
      14,    66,    33,    33,    27,     3,   108,    34,    99,    99,
     104,   105,    11,    12,    30,    37,    50,    92,    38,    34,
      30,    99,   106,    36,     3,    35,    54,    55,    99,    33,
      35,    66,    66,     4,   109,   110,     3,     3,    34,    67,
      72,     3,     3,    19,    20,    34,    43,    74,    75,    76,
      14,    42,    74,    27,    27,    49,    34,    50,     3,    35,
      39,    36,    99,    99,     3,    22,    22,    97,    98,    99,
       3,    99,    36,    36,   103,    37,    35,    36,    50,    39,
      33,     4,    16,    75,    36,    74,    49,    49,    28,     3,
      22,    43,    85,    86,    87,    90,    36,    99,    50,    36,
      39,    36,    79,    50,    35,    99,    99,    35,    99,    55,
      13,    22,    27,    56,   111,    68,     4,   110,    36,     3,
      35,    36,    76,    28,    28,    33,    88,     3,    43,    35,
      36,   103,    88,    38,   100,    98,     3,    80,    81,   105,
      35,    29,    57,    58,   111,    50,     4,    67,    33,     4,
      35,    35,    99,    37,    89,     3,    21,    91,    50,    34,
      39,   101,   102,    35,    37,    36,    36,    57,    28,     3,
      51,    61,    62,    63,    69,    77,    82,   110,    35,    36,
       3,     4,    22,    99,    33,    93,    94,    87,     3,    36,
     103,    99,     3,    81,    80,    28,    37,    64,    65,    33,
       4,    27,    92,   111,    36,   102,    39,    33,    33,    27,
      35,     3,    17,    29,    95,    96,   111,    27,   111,    92,
      99,    27,    27,    58,    37,    99,    28,    28,    96,    28,
      95,   111,    36,   103,    58,    58,    28,    99,    34,    28,
      28,    35,    28,    28,    35
  };

  const unsigned char
  parser::yyr1_[] =
  {
       0,    46,    47,    47,    48,    49,    49,    49,    49,    49,
      49,    49,    49,    50,    50,    51,    52,    53,    53,    53,
      54,    54,    55,    55,    56,    56,    56,    57,    57,    58,
      58,    58,    58,    58,    58,    59,    59,    60,    60,    61,
      61,    62,    62,    63,    64,    65,    66,    66,    66,    66,
      66,    66,    66,    67,    67,    67,    68,    68,    68,    68,
      68,    68,    69,    69,    69,    69,    69,    69,    69,    69,
      70,    70,    70,    70,    71,    71,    72,    72,    73,    73,
      74,    74,    74,    75,    75,    76,    76,    76,    76,    76,
      77,    78,    79,    79,    79,    79,    80,    80,    81,    82,
      83,    83,    84,    85,    85,    86,    86,    87,    87,    87,
      87,    88,    88,    89,    89,    89,    89,    90,    90,    91,
      91,    92,    93,    93,    93,    94,    94,    94,    94,    94,
      94,    94,    95,    95,    96,    96,    96,    97,    97,    98,
      98,    99,    99,    99,    99,    99,    99,    99,    99,    99,
     100,   100,   101,   101,   102,   103,   103,   104,   104,   105,
     105,   106,   106,   107,   107,   107,   108,   108,   109,   109,
     109,   110,   110,   111,   111
  };

  const unsigned char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     6,     1,     3,     2,     0,
       3,     1,     1,     3,     2,     3,     4,     1,     1,     2,
       2,     2,     2,     2,     0,     6,     1,     5,     6,     6,
       1,     5,     6,     2,     2,     1,     3,     3,     6,     6,
       3,     3,     3,     4,     5,     7,     1,     1,     1,     1,
       1,     1,     3,     3,     3,     3,     3,     6,     4,     6,
       2,     4,     4,     5,     3,     1,     1,     3,     1,     2,
       1,     3,     4,     3,     1,     1,     1,     1,     1,     3,
       3,     7,     0,     2,     2,     4,     3,     1,     3,     8,
       2,     0,     3,     2,     0,     4,     1,     3,     1,     2,
       1,     2,     0,     2,     2,     2,     0,     2,     3,     2,
       0,     2,     5,     4,     1,     2,     3,     3,     5,     4,
       4,     0,     2,     1,     3,     2,     4,     3,     1,     1,
       1,     1,     4,     3,     6,     3,     3,     3,     1,     1,
       4,     2,     3,     1,     6,     1,     0,     1,     0,     3,
       1,     3,     3,     4,     4,     2,     1,     3,     1,     3,
       5,     1,     0,     1,     1
  };



  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a yyntokens_, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "$undefined", "NAME", "NUMBER", "LEXERROR",
  "CLASS", "DEF", "ELSE", "ELIF", "IF", "OR", "AND", "PASS", "IMPORT",
  "FROM", "AS", "RAISE", "NOTHING", "NAMEDTUPLE", "TYPEVAR", "ARROW",
  "ELLIPSIS", "EQ", "NE", "LE", "GE", "INDENT", "DEDENT", "TRIPLEQUOTED",
  "TYPECOMMENT", "BYTESTRING", "UNICODESTRING", "':'", "'('", "')'", "','",
  "'='", "'['", "']'", "'<'", "'>'", "'.'", "'*'", "'@'", "'?'", "$accept",
  "start", "unit", "alldefs", "maybe_type_ignore", "classdef",
  "class_name", "parents", "parent_list", "parent", "maybe_class_funcs",
  "class_funcs", "funcdefs", "if_stmt", "if_and_elifs", "class_if_stmt",
  "class_if_and_elifs", "if_cond", "elif_cond", "else_cond", "condition",
  "version_tuple", "condition_op", "constantdef", "importdef",
  "import_items", "import_item", "import_name", "from_list", "from_items",
  "from_item", "alias_or_constant", "typevardef", "typevar_args",
  "typevar_kwargs", "typevar_kwarg", "funcdef", "decorators", "decorator",
  "params", "param_list", "param", "param_type", "param_default",
  "param_star_name", "return", "typeignore", "maybe_body", "empty_body",
  "body", "body_stmt", "type_parameters", "type_parameter", "type",
  "named_tuple_fields", "named_tuple_field_list", "named_tuple_field",
  "maybe_comma", "maybe_type_list", "type_list", "type_tuple_elements",
  "type_tuple_literal", "dotted_name", "getitem_key", "maybe_number",
  "pass_or_ellipsis", YY_NULLPTR
  };

#if YYDEBUG
  const unsigned short int
  parser::yyrline_[] =
  {
       0,   132,   132,   133,   137,   141,   142,   143,   144,   150,
     151,   152,   157,   161,   162,   168,   175,   186,   187,   188,
     192,   193,   197,   198,   202,   203,   204,   208,   209,   213,
     214,   219,   220,   225,   226,   231,   234,   239,   243,   262,
     265,   270,   274,   286,   290,   294,   298,   301,   304,   307,
     310,   311,   312,   317,   318,   319,   325,   326,   327,   328,
     329,   330,   334,   338,   342,   346,   350,   354,   358,   362,
     369,   373,   377,   383,   392,   393,   396,   397,   402,   403,
     410,   411,   412,   416,   417,   421,   422,   425,   428,   431,
     435,   439,   446,   447,   448,   449,   453,   454,   458,   462,
     479,   480,   484,   488,   489,   501,   502,   506,   507,   508,
     509,   513,   514,   518,   519,   520,   521,   525,   526,   530,
     531,   535,   539,   540,   541,   545,   546,   547,   548,   549,
     550,   551,   555,   556,   560,   561,   562,   566,   567,   571,
     572,   576,   580,   584,   589,   593,   594,   595,   596,   597,
     601,   602,   606,   607,   611,   615,   616,   620,   621,   625,
     626,   633,   634,   643,   648,   654,   661,   662,   676,   677,
     682,   690,   691,   695,   696
  };

  // Print the state stack on the debug stream.
  void
  parser::yystack_print_ ()
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << i->state;
    *yycdebug_ << std::endl;
  }

  // Report on the debug stream that the rule \a yyrule is going to be reduced.
  void
  parser::yy_reduce_print_ (int yyrule)
  {
    unsigned int yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):" << std::endl;
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // YYDEBUG

  // Symbol number corresponding to token number t.
  inline
  parser::token_number_type
  parser::yytranslate_ (int t)
  {
    static
    const token_number_type
    translate_table[] =
    {
     0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      34,    35,    43,     2,    36,     2,    42,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    33,     2,
      40,    37,    41,    45,    44,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    38,     2,    39,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32
    };
    const unsigned int user_token_number_max_ = 287;
    const token_number_type undef_token_ = 2;

    if (static_cast<int>(t) <= yyeof_)
      return yyeof_;
    else if (static_cast<unsigned int> (t) <= user_token_number_max_)
      return translate_table[t];
    else
      return undef_token_;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:1167
} // pytype
#line 2834 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:1167
#line 699 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:1168


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace
